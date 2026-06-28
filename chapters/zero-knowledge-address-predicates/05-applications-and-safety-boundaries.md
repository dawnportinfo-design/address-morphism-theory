# Applications and Safety Boundaries

## Private Delivery

An ecommerce site may receive only:

- alias
- deliverability class
- nullifier
- receipt handle

The carrier can receive a separate decryptable envelope if the holder consents.

## Hotel and PMS

A hotel system can verify that an address credential is fresh and jurisdiction
compatible without storing the raw guest address by default.

## POS and Locker

POS and locker systems should display acceptance decisions and receipts, not QR
payload internals or hidden address text.

## Web3 Boundary

On-chain systems should store only commitments, roots, registry pointers, or
revocation anchors. Raw address, witness, and precise coordinate data are out of
scope for public chains.
