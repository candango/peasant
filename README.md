# Candango Peasant

Peasant is a protocol abstraction of how to control agents that need to
communicate with a central entity or entities.

We define agents as peasants and central entities(bases) as bastions.

This project won't define the implementation, security level neither levels of
redundancies but instead a minimal contract of what should be implemented.

A bastion/peasant relationship could be defined as stateful or not. If stateful
it is necessary to implement a session control in the bastion where peasants
need to perform knocks(as knock at the door) in order to get permission or a
valid session. In a stateless case we just ignore any knock implementation.

What must be implemented in the protocol are nonce generation, consumption and
validation on both sides and a directory list of available resources offered by
a bastion for peasants to consume.

## Support

Automatoes is one of
[Candango Open Source Group](http://www.candango.org/projects/)
initiatives. Available under the
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).

This web site and all documentation is licensed under
[Creative Commons 3.0](http://creativecommons.org/licenses/by/3.0/).

Copyright © 2020 Flavio Goncalves Garcia
