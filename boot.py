#!/usr/bin/env python

""" Creates a 512MB server and uploads a public key to it. Requires pyrax

Usage:
  boot.py <name> <public_key> [--image=<name>]

Arguments:
  <name>          Name of the server.
  <public_key>    Path to your SSH public key.

Options:
  -h --help       Show this screen.
  --image=<name>  Name of an image. [default: Ubuntu 13.04]

"""

from docopt import docopt
import pyrax

args = docopt(__doc__, help = True)
pyrax.keyring_auth()
cs = pyrax.cloudservers

key = open(args['<public_key>'])
public_key = {'/root/.ssh/authorized_keys': key}

image = next(img for img in cs.images.list() if args['--image'] in img.name)

build = cs.servers.create(args['<name>'],
	image.id, 2, files = public_key)

server = pyrax.utils.wait_until(build, "status", ["ACTIVE", "ERROR"],
				attempts = 0, interval = 20, verbose = True)

print "--"
print "Public IP address: ", server.networks['public'][0]
