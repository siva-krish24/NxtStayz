"""Main module."""
import argparse
import logging
import os

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from ccbp_ide_cli.cli_functions.ccbp_authenticate import CCBPAuthenticate
from ccbp_ide_cli.cli_functions.ccbp_backup import CCBPBackup
from ccbp_ide_cli.cli_functions.ccbp_logout import CCBPLogout
from ccbp_ide_cli.cli_functions.ccbp_publish import CCBPPublish
from ccbp_ide_cli.cli_functions.ccbp_reset import CCBPReset
from ccbp_ide_cli.cli_functions.ccbp_solution import CCBPSolution
from ccbp_ide_cli.cli_functions.ccbp_start import CCBPStart
from ccbp_ide_cli.cli_functions.ccbp_stop import CCBPStop
from ccbp_ide_cli.cli_functions.ccbp_submit import CCBPSubmit
from ccbp_ide_cli.cli_functions.ccbp_update import CCBPUpdate
from ccbp_ide_cli.cli_functions.ccbp_version import CCBPVersion
from ccbp_ide_cli.utils.output_utils import enable_cursor

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.CRITICAL,
)
sentry_sdk.init(
    dsn="https://ba2e638ca2475bd560849a4b8406b562@o1177444.ingest.sentry.io/4506222887829505",
    integrations=[sentry_logging],
    environment=os.environ.get('BACKEND_STAGE'),
    debug=False,
)


# pylint: disable=too-many-branches, too-many-statements
def main():  # noqa: C901, PLR0912, PLR0915
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)

    authenticate = subparser.add_parser('authenticate')
    authenticate.add_argument("ide_token", type=str, help="Enter IDE Token")

    start = subparser.add_parser('start')
    start.add_argument('session_id', type=str, help="Enter Session ID")

    submit = subparser.add_parser('submit')
    submit.add_argument('session_id', type=str, help="Enter Session ID")

    solution = subparser.add_parser('solution')
    solution.add_argument('session_id', type=str, help="Enter Session ID")

    publish = subparser.add_parser('publish')
    publish.add_argument('session_id', type=str, help="Enter Session ID")
    publish.add_argument('domain_url', type=str, help="Enter Domain URL")

    stop = subparser.add_parser('stop')
    stop.add_argument(
        'drop_instance_id', type=str, help="Enter Drop Instance ID")
    stop.add_argument('stop_reason', type=str, help="Enter Stop Reason")

    reset = subparser.add_parser('reset')
    reset.add_argument('session_id', type=str, help="Enter Session ID")

    update = subparser.add_parser('update')
    update.add_argument('reusable_session_id', type=str, help="Enter Reusable Session ID")
    update.add_argument('current_session_id', type=str, help="Enter Current Session ID")

    subparser.add_parser('backup')

    subparser.add_parser('logout')

    subparser.add_parser('version')

    args = parser.parse_args()

    if args.command.lower() == "authenticate":
        if args.ide_token:
            ccbp_authenticate = CCBPAuthenticate()
            ccbp_authenticate.ccbp_authenticate(ide_token=args.ide_token)
    elif args.command.lower() == "start":
        if args.session_id:
            ccbp_start = CCBPStart()
            ccbp_start.ccbp_start(session_display_id=args.session_id)
    elif args.command.lower() == "reset":
        if args.session_id:
            ccbp_reset = CCBPReset()
            ccbp_reset.ccbp_reset(session_display_id=args.session_id)
    elif args.command.lower() == "submit":
        if args.session_id:
            ccbp_submit = CCBPSubmit()
            ccbp_submit.ccbp_submit(session_display_id=args.session_id)
    elif args.command.lower() == "solution":
        if args.session_id:
            ccbp_submit = CCBPSolution()
            ccbp_submit.ccbp_solution(session_display_id=args.session_id)
    elif args.command.lower() == "logout":
        ccbp_logout = CCBPLogout()
        ccbp_logout.ccbp_logout()
    elif args.command.lower() == "version":
        ccbp_version = CCBPVersion()
        ccbp_version.ccbp_version()
    elif args.command.lower() == "publish":
        if args.session_id and args.domain_url:
            ccbp_publish = CCBPPublish()
            ccbp_publish.ccbp_publish(
                session_display_id=args.session_id, domain_url=args.domain_url)
    elif args.command.lower() == "stop":
        if args.drop_instance_id and args.stop_reason:
            ccbp_stop = CCBPStop()
            ccbp_stop.ccbp_stop(
                drop_instance_id=args.drop_instance_id,
                stop_reason=args.stop_reason)
    elif args.command.lower() == "update":
        if args.reusable_session_id and args.current_session_id:
            ccbp_update = CCBPUpdate()
            ccbp_update.ccbp_update(
                reusable_session_id=args.reusable_session_id,
                current_session_id=args.current_session_id)
    elif args.command.lower() == "backup":
        ccbp_update = CCBPBackup()
        ccbp_update.ccbp_backup()
    else:
        parser.print_help()

    enable_cursor()


if __name__ == "__main__":
    main()
