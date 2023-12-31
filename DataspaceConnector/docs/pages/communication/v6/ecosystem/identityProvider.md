---
layout: default
title: Identity Provider
nav_order: 1
description: ""
permalink: /CommunicationGuide/v6/IdsEcosystem/IdentityProvider
parent: IDS Ecosystem
grand_parent: Communication Guide
---

# IDS Identity Provider
{: .fs-9 }

This section provides a detailed guide on communication with the IDS Identity Provider.
The Identity Provider consists of the Certification Authority (CA), the
Dynamic Attribute Provisioning Service (DAPS) and the Participant Information System (ParIS).
{: .fs-6 .fw-300 }

---

## Dynamic Attribute Provisioning Service (DAPS)

IDS connectors request a digitally signed JSON web token (JWT) from a central IDS component called
Dynamic Attribute Provisioning Service (DAPS) in order to authenticate themselves. Without these
DAPS tokens (DATs) no connector can participate in the IDS.

The Dataspace Connector communicates with the DAPS provided by the Fraunhofer AISEC by default. It
is available at [https://daps.aisec.fraunhofer.de/](https://daps.aisec.fraunhofer.de/).

The [repository](https://github.com/International-Data-Spaces-Association/omejdn-daps) is open
source and can be accessed at GitHub. Further documentation about the IDS Identity Provider/DAPS can
be seen [here](https://github.com/International-Data-Spaces-Association/IDS-G/blob/main/Components/IdentityProvider/README.md).
The content of a Dynamic Attribute Token (DAT) is listed and explained
[here](https://github.com/International-Data-Spaces-Association/IDS-G/blob/main/Components/IdentityProvider/DAPS/README.md#dynamic-attribute-token-content).

### AISEC DAPS: Issuing an IDS certificate

If you want to locally test a certain setup of IDS connectors, there is some sample key material
available for localized docker domains such as (provider-core or consumer-core) which can be
downloaded [here](https://github.com/industrial-data-space/trusted-connector/tree/master/examples/etc),
or as complete sample set [here](https://github.com/industrial-data-space/trusted-connector/blob/master/examples/trusted-connector-examples_latest.zip).

If you want to run your IDS-connector on an internet domain, such as connector.aisec.fraunhofer.de,
for instance, there are two steps involved to receive your key material to authenticate at the IDS
DAPS:

1. Please register for a Github Account and for the International Dataspaces Association (use the contact form) on the
   [website](https://internationaldataspaces.org) and wait for approval.

2. How to Submit Requests: please send a mail to [daps-certificates@aisec.fraunhofer.de](mailto:daps-certificates@aisec.fraunhofer.de) with the following necessary pieces of information for the DAPS certificate request:
   - Country,
   - Organization,
   - Organizational Unit,
   - Domain,
   - and if the entry shall be published within the IDS community (default yes).
     Afterwards, you will receive the certificate and its corresponding key material bundled as .p12-archive via e-mail.

Afterwards, you will receive the certificate and its corresponding key material bundled as
.p12-archive via e-mail.

A mailing list dealing with DAPS certificates and questions regarding the key material (not the setup of connectors) is the same as for requesting certificates [daps-certificates@aisec.fraunhofer.de](mailto:daps-certificates@aisec.fraunhofer.de).

## Participant Information System (ParIS)

The Participant Information System (ParIS) is available at [https://paris.ids.isst.fraunhofer.de](https://paris.ids.isst.fraunhofer.de).
It expects IDS multipart messages at [https://paris.ids.isst.fraunhofer.de/infrastructure](https://paris.ids.isst.fraunhofer.de/infrastructure).
The GUI can be accessed at [https://paris.ids.isst.fraunhofer.de/browse](https://paris.ids.isst.fraunhofer.de/browse).
To get your IP address unblocked, please contact [us](mailto:info@dataspace-connector.de).

The [repository](https://github.com/International-Data-Spaces-Association/ParIS-open-core) is open
core and can be accessed at GitHub. Further documentation about the ParIS can be seen
[here](https://github.com/International-Data-Spaces-Association/IDS-G/blob/main/Components/IdentityProvider/ParIS/README.md).

The Dataspace Connector currently does not offer any ParIS interaction.
