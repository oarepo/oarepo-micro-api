# -*- coding: utf-8 -*-
#
# Copyright (C) 2018-2020 CERN.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI for Invenio App ILS."""
import random
from uuid import uuid4

import click
import lorem
import names
import redis
from flask.cli import with_appcontext
from invenio_accounts.models import User
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.models import PIDStatus, PersistentIdentifier
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_search import current_search
from invenio_userprofiles import UserProfile

from video_repository_api.records.api import Record
from video_repository_api.records.constants import ACL_PREFERRED_SCHEMA


def minter(pid_type, pid_field, record):
    """Mint the given PID for the given record."""
    pid = PersistentIdentifier.get(
        pid_type="recid",
        pid_value=record[pid_field]
    )
    pid.status = PIDStatus.REGISTERED
    pid.object_type = "rec"
    pid.object_uuid = record.id
    pid.pid_type = pid_type


def create_userprofile_for(email, username, full_name):
    """Create a user profile."""
    user = User.query.filter_by(email=email).one_or_none()
    if user:
        profile = UserProfile(user_id=int(user.get_id()))
        profile.username = username
        profile.full_name = full_name
        db.session.add(profile)
        db.session.commit()


def random_lang():
    """Create a random language."""
    return random.choice(['en', 'cs', 'de', 'fr', 'es'])


class Holder(object):
    """Holds generated data."""

    def __init__(self, total_items):
        """Constructor."""
        self.items = {"objs": [], "total": total_items}

    def pids(self, collection, pid_field):
        """Get a list of PIDs for a collection."""
        return [obj[pid_field] for obj in getattr(self, collection)["objs"]]


class Generator(object):
    """Generator."""

    def __init__(self, holder):
        """Constructor."""
        self.holder = holder
        # self.minter = minter

    def create_pid(self):
        """Create a new persistent identifier."""
        return RecordIdProviderV2.create().pid.pid_value

    def _persist(self, pid_type, pid_field, record):
        """Mint PID and store in the db."""
        minter(pid_type, pid_field, record)
        record.commit()
        return record


class ItemGenerator(Generator):
    """Item Generator."""

    def generate(self):
        """Generate."""
        size = self.holder.items["total"]
        objs = [
            {
                "owners": [-1],
                "pid": self.create_pid(),
                "identifier": "{}".format(uuid4()),
                "abstract": [{"lang": random_lang(), "value": lorem.text()}],
                "title": [{"lang": random_lang(), "value": lorem.sentence()}],
                "description": [{"lang": random_lang(), "value": lorem.paragraph()}],
                "creator": names.get_full_name(random.choice(['male', 'female'])),
                "contributor": names.get_full_name(random.choice(['male', 'female'])),
                "language": random_lang(),
            }
            for pid in range(1, size + 1)
        ]

        self.holder.items["objs"] = objs

    def persist(self):
        """Persist."""
        recs = []
        for obj in self.holder.items["objs"]:
            rec = self._persist("recid", "pid", Record.create(obj))
            recs.append(rec)
        db.session.commit()
        return recs


@click.group()
def demo():
    """Demo data CLI."""


@demo.command()
@click.option("--items", "n_items", default=50)
@with_appcontext
def data(n_items):
    """Insert demo data."""
    click.secho("Generating demo data", fg="yellow")

    indexer = RecordIndexer()
    holder = Holder(
        total_items=n_items,
    )

    click.echo("Creating items...")
    items_generator = ItemGenerator(holder)
    items_generator.generate()
    rec_items = items_generator.persist()
    for rec in rec_items:
        # TODO: bulk index when we have the queue
        indexer.index(rec)

    current_search.flush_and_refresh(index="*")


@click.command()
@click.argument('admin_password')
@click.option("--recreate-db", is_flag=True, help="Recreating DB.")
@click.option(
    "--skip-demo-data", is_flag=True, help="Skip creating demo data."
)
@click.option(
    "--skip-file-location",
    is_flag=True,
    help="Skip creating file location."
)
@click.option("--verbose", is_flag=True, help="Verbose output.")
@with_appcontext
def setup(admin_password, recreate_db, skip_demo_data, skip_file_location, verbose):
    """OARepo setup command."""
    from flask import current_app
    from invenio_base.app import create_cli

    click.secho("oarepo setup started...", fg="blue")

    # Clean redis
    redis.StrictRedis.from_url(
        current_app.config["CACHE_REDIS_URL"]
    ).flushall()
    click.secho("redis cache cleared...", fg="red")

    cli = create_cli()
    runner = current_app.test_cli_runner()

    def run_command(command, catch_exceptions=False):
        click.secho("oarepo {}...".format(command), fg="green")
        res = runner.invoke(cli, command, catch_exceptions=catch_exceptions)
        if verbose:
            click.secho(res.output)

    # Remove and create db and indexes
    if recreate_db:
        run_command("db destroy --yes-i-know", catch_exceptions=True)
        run_command("db init")
    else:
        run_command("db drop --yes-i-know")
    run_command("db create")
    run_command("index destroy --force --yes-i-know")
    run_command("index init --force")
    # run_command("index queue init purge")

    # Create roles to restrict access
    run_command("roles create admin")

    # Create users
    run_command(
        "users create admin@oarepo.org -a --password={}".format(admin_password)
    )  # ID 1
    create_userprofile_for("admin@oarepo.org", "admin", "OArepo Administrator")

    # Assign roles
    run_command("roles add admin@oarepo.org admin")

    # Assign actions
    run_command("access allow superuser-access role admin")

    # Create files location
    if not skip_file_location:
        run_command("files location --default oarepo /tmp/oarepo")

    # Create ACLs index for preferred SCHEMA
    run_command("invenio invenio_explicit_acls prepare {}".format(ACL_PREFERRED_SCHEMA))

    # Generate demo data
    if not skip_demo_data:
        run_command("demo data")

    click.secho("oarepo setup finished successfully", fg="blue")
