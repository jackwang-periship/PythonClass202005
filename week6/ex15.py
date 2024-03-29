import paramiko


def create_sftp_client(host, port, username, password, keyfilepath, keyfiletype):
    """
    create_sftp_client(host, port, username, password, keyfilepath, keyfiletype) -> SFTPClient

    Creates a SFTP client connected to the supplied host on the supplied port authenticating as the user with
    supplied username and supplied password or with the private key in a file with the supplied path.
    If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
    :rtype: SFTPClient object.
    """
    sftp = None
    key = None
    transport = None
    try:
        if keyfilepath is not None:
            # Get private key used to authenticate user.
            if keyfiletype == 'DSA':
                # The private key is a DSA type key.
                key = paramiko.DSSKey.from_private_key_file(keyfilepath)
            else:
                # The private key is a RSA type key.
                key = paramiko.RSAKey.from_private_key(keyfilepath)

        # Create Transport object using supplied method of authentication.
        transport = paramiko.Transport((host, port))
        transport.connect(None, username, password, key)

        sftp = paramiko.SFTPClient.from_transport(transport)

        return sftp
    except Exception as e:
        print('An error occurred creating SFTP client: %s: %s' % (e.__class__, e))
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()
        pass


host, port = "periship.exavault.com", 22
username, password = "jack.wang888@gmail.com", "Jackwang1"
keyfile_path = None

sftpclient = create_sftp_client(host, port, username, password, keyfile_path, 'DSA')

sftpclient.put('ftpsftp.py', 'In/remote_ftpsftp.py')

# Retrieve a file with the name 'remote_file.txt' on the remote computer
# and store it in a file named 'downloaded_file.txt'
# next to this SFT client program.
sftpclient.get('Out/remote_file.txt', 'downloaded_file.txt')

sftpclient.close()
print('Done!')
