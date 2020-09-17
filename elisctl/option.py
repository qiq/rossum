from typing import Optional, Callable

import click

from elisctl.common import schema_content_factory
from click_option_group import optgroup, AllOptionGroup


organization = click.option(
    "-o", "--organization-id", type=int, help="Organization ID.", hidden=True
)

name = click.option("-n", "--name", type=str)
email_prefix = click.option(
    "--email-prefix", type=str, help="If not specified, documents cannot be imported via email."
)
bounce_email = click.option(
    "--bounce-email", type=str, help="Unprocessable documents will be bounced to this email."
)
connector_id = click.option(
    "--connector-id", type=str, help="If not specified, queue will not call back a connector."
)

hook_id = click.option(
    "--hook-id",
    type=int,
    multiple=True,
    help="If not specified, hook will not be associated with the queue.",
)

output_file = click.option("-O", "--output-file", type=click.File("wb"))


def schema_content_file(command: Optional[Callable] = None, **kwargs):
    default_kwargs = {"type": click.File("rb"), "help": "Schema file."}
    kwargs = {**default_kwargs, **kwargs}
    decorator = click.option("-s", "--schema-content-file", "schema_content_file_", **kwargs)
    if command is None:
        return decorator
    return decorator(command)


schema_content = schema_content_factory(schema_content_file)


def workspace_id(command: Optional[Callable] = None, **kwargs):
    default_kwargs = {"type": int, "help": "Workspace ID."}
    kwargs = {**default_kwargs, **kwargs}
    decorator = click.option("-w", "--workspace-id", **kwargs)
    if command is None:
        return decorator
    return decorator(command)


def queue(command: Optional[Callable] = None, related_object: Optional[str] = "object", **kwargs):
    default_kwargs = {
        "type": int,
        "help": f"Queue IDs, which the {related_object} will be associated with.",
        "multiple": True,
        "show_default": True,
    }
    kwargs = {**default_kwargs, **kwargs}
    decorator = click.option("-q", "--queue-id", "queue_ids", **kwargs)
    if command is None:
        return decorator
    return decorator(command)


def user(command: Optional[Callable] = None, **kwargs):
    default_kwargs = {
        "type": int,
        "multiple": True,
        "help": "User IDs, which the queues will be associated with.",
    }
    kwargs = {**default_kwargs, **kwargs}
    decorator = click.option("-u", "--user-id", "user_ids", **kwargs)
    if command is None:
        return decorator
    return decorator(command)


service_url = click.option(
    "-u", "--service-url", type=str, required=True, help="Url of the connector endpoint."
)

auth_token = click.option(
    "-t",
    "--auth-token",
    type=str,
    help="Token sent to the connector in the header to ensure authorization. "
    "Generated automatically, if not set manually.",
)

params = click.option("-p", "--params", type=str, help="Query params appended to the service_url.")

asynchronous = click.option(
    "-a", "--asynchronous", type=bool, default=True, help="Affects calling of the connector."
)

active = click.option(
    "--active", type=bool, required=True, default=True, help="Affects whether the hook is notified."
)

events = click.option(
    "-e",
    "--events",
    required=True,
    type=str,
    multiple=True,
    help="List of events, when the hook should be notified.",
)


hook_type = click.option(
    "--type",
    required=True,
    default="webhook",
    type=click.Choice(["function", "webhook"]),
    help="Hook type. Possible values: webhook, function.",
)

webhook_option_group = optgroup.group(
    "Webhook options", cls=AllOptionGroup, help="Group description"
)

config_url = optgroup.option(
    "--config-url", type=str, help="URL endpoint where the message from the hook should be pushed."
)

config_secret = optgroup.option(
    "--config-secret", type=str, default=None, help="Secret key for authorization of payloads."
)

config_insecure_ssl = optgroup.option(
    "--config_insecure_ssl",
    type=bool,
    default=False,
    help="Disable SSL certificate verification. (Use only for testing purposes.)",
)

function_option_group = optgroup.group(
    "Function options", cls=AllOptionGroup, help="Group description"
)

config_code = optgroup.option(
    "--config-code", type=str, default=None, help="String-serialized source code to be executed."
)

config_runtime = optgroup.option(
    "--config-runtime",
    type=str,
    default="nodejs12.x.",
    help="Runtime used to execute code. Allowed values: nodejs12.x.",
)


def group(command: Optional[Callable] = None, **kwargs):
    default_kwargs = {
        "default": "annotator",
        "type": click.Choice(["annotator", "admin", "manager", "viewer"]),
        "help": "Permission group.",
        "show_default": True,
    }
    kwargs = {**default_kwargs, **kwargs}
    decorator = click.option("-g", "--group", **kwargs)
    if command is None:
        return decorator
    return decorator(command)


def locale(command: Optional[Callable] = None, **kwargs):
    default_kwargs = {
        "default": "en",
        "type": click.Choice(["en", "cs"]),
        "help": "UI locale",
        "show_default": True,
    }
    kwargs = {**default_kwargs, **kwargs}
    decorator = click.option("-l", "--locale", **kwargs)
    if command is None:
        return decorator
    return decorator(command)


def password(command: Optional[Callable] = None, **kwargs):
    default_kwargs = {"type": str, "required": False, "help": "Generated, if not specified."}
    kwargs = {**default_kwargs, **kwargs}
    if "help" in kwargs and kwargs["help"] is None:
        kwargs.pop("help")
    decorator = click.option("-p", "--password", **kwargs)
    if command is None:
        return decorator
    return decorator(command)
