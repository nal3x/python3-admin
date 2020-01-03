from argparse import ArgumentParser, Action

known_drivers = ['local', 's3']

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error(f"Unknown driver. Available drivers are {', '.join(known_drivers)}")
        namespace.driver = driver.lower()
        namespace.destination = destination


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('url', help="URL of the PostgreSQL database to backup")
    parser.add_argument('--driver', '-d',
            help="how & where to store the backup",
            nargs=2,
            action=DriverAction,
            required=True,
            metavar=('driver', 'destination'))
    return parser

def main():
    import boto3
    import time
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    if args.driver == 's3':
        client = boto3.client('s3')
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        filename = pgdump.dump_file_name(args.url, timestamp)
        storage.s3(client, dump.stdout, args.destination, filename)
        print(f"Backing database to bucket {args.destination} in S3 as {filename}")
    else:
        outfile = open(args.destination, 'wb')
        print(f"Backing database locally as {args.destination}")
        storage.local(dump.stdout, outfile)

