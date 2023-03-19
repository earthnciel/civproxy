# civproxy
A serial communication link program that supports PTT CAT commands in an omnirig for old ICOM rig


[Omnirig] -- [com0com] -- [rig]

example
Omnirig : com4
com0com : com4 -- com5 (virtual pair)
rig : com10

Premise:
Assign RTS to TX signal


old rig's ini file (omnirig):
Command must end with 0xFD (CI-V protocol)

AS-IS
----------------------------------------------------------
[pmRx]
;not supported

[pmTx]
;not supported
----------------------------------------------------------


TO-BE
----------------------------------------------------------
[pmRx]
Command=FEFE28E0.1C00.00.FD
ReplyLength=0

[pmTx]
Command=FEFE28E0.1C00.01.FD
ReplyLength=0
----------------------------------------------------------


config.py
----------------------------------------------------------
CONFIG = {
    # RX/TX command
    'rx_command': b'\xFE\xFE\x28\xE0\x1C\x00\x00\xFD',
    'tx_command': b'\xFE\xFE\x28\xE0\x1C\x00\x01\xFD',
    
    .....
----------------------------------------------------------

