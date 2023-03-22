# civproxy
A serial communication link program that supports PTT CAT commands in an omnirig for old ICOM rig
<br>
<br>
# connection
[Omnirig] -- [com0com] -- [CI-V interface] -- [rig]<br>
<br>
example<br>
Omnirig : com4<br>
com0com : com4 -- com5 (virtual pair)<br>
CI-V interface : com10<br>
rig : ci-v<br>
<br>
# Premise:
Assign RTS to TX signal<br>
<br>
<br>
# old rig's ini file (omnirig):
Command must end with 0xFD (CI-V protocol)<br>
<br>
AS-IS
<pre>
[pmRx]<br>
;not supported<br>
<br>
[pmTx]<br>
;not supported<br>
</pre>


TO-BE
<pre>
[pmRx]<br>
Command=FEFE28E0.1C00.00.FD<br>
ReplyLength=0<br>
<br>
[pmTx]<br>
Command=FEFE28E0.1C00.01.FD<br>
ReplyLength=0<br>
</pre>
<br>

# config.py
<pre>
CONFIG = {<br>
    # RX/TX command<br>
    'rx_command': b'\xFE\xFE\x28\xE0\x1C\x00\x00\xFD',<br>
    'tx_command': b'\xFE\xFE\x28\xE0\x1C\x00\x01\xFD',<br>
    <br>
    .....<br>
</pre>

