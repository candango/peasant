# Candango Peasant

Peasant is a protocol abstraction of how to control agents that need to
communicate with a central entity or entities.

We define agents as peasants and central entities (bases) as bastions.

Peasant will define some transport definition to help developer with basic http
methods (i.e. head, post, get, etc), and avoid code duplication. Security level
and your business should be implemented.

A bastion/peasant relationship could be defined as stateful or not. If stateful
it is necessary to implement a session control in the bastion where peasants
need to perform knocks (as knock at the door) to get permission or a valid
session. In a stateless case we just ignore any knock implementation.

What must be implemented in the protocol are nonce generation, consumption and
validation on both sides. A directory list of available resources offered by
a bastion for peasants to consume could also be useful to have.

## Support

Peasant is one of
[Candango Open Source Group](http://www.candango.org/projects/)
initiatives. Available under the
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).

This website and all documentation are licensed under
[Creative Commons 3.0](http://creativecommons.org/licenses/by/3.0/).

Copyright © 2020-2024 Flavio Garcia
