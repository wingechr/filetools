# ssh

* `addgroup ssh-users`
* `adduser USER ssh-users`
* make sure you have a connection with root while testing!
* make sure you have you users public key in `$HOME/.ssh/authorized_keys` with permissions set to 700

* edit `/etc/ssh/sshd_config`

```
Port 22
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
LogLevel INFO
PermitRootLogin no
AllowGroups ssh-users
StrictModes yes
MaxAuthTries 3
# AuthenticationMethods publickey
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
PrintMotd no
UsePrivilegeSeparation sandbox
Banner none
AcceptEnv LANG LC_*
Subsystem       sftp    /usr/lib/openssh/sftp-server
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com
```
