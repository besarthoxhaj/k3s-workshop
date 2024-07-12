## Public Key Infrastructure (PKI)


```sh
$ base64 --decode -i ./foo.txt -o ./bar.txt
$ openssl x509 -in ./bar.txt -noout -text
# Certificate:
#     Data:
#         Version: 3 (0x2)
#         Serial Number:
#             48:B0:E3:6B:DA...
#         Signature Algorithm: sha256WithRSAEncryption
#         Issuer: C=US, O=Let's Encrypt, CN=R11
#         Validity
#             Not Before: Jul  8 15:18:08 2024 GMT
#             Not After : Oct  6 15:18:07 2024 GMT
#         Subject: CN=mlx.today
#         Subject Public Key Info:
#             Public Key Algorithm: rsaEncryption
#                 Public-Key: (2048 bit)
#                 Modulus:
#                     48:B0:E3:6B:DA...
#                 Exponent: 65537 (0x10001)
#         X509v3 extensions:
#             X509v3 Key Usage: critical
#                 Digital Signature, Key Encipherment
#             X509v3 Extended Key Usage:
#                 TLS Web Server Authentication, TLS Web Client Authentication
#             X509v3 Basic Constraints: critical
#                 CA:FALSE
#             X509v3 Subject Key Identifier:
#                 48:B0:E3:6B:DA...
#             X509v3 Authority Key Identifier:
#                 48:B0:E3:6B:DA...
#             Authority Information Access:
#                 OCSP - URI:http://r11.o.lencr.org
#                 CA Issuers - URI:http://r11.i.lencr.org/
#             X509v3 Subject Alternative Name:
#                 DNS:mlx.today
#             X509v3 Certificate Policies:
#                 Policy: 2.23.140.1.2.1
#             CT Precertificate SCTs:
#                 Signed Certificate Timestamp:
#                     Version   : v1 (0x0)
#                     Log ID    : 3F:17:4B:4F:D7:22:47:58:94:1D...
#                     Timestamp : Jul  8 16:18:08.996 2024 GMT
#                     Extensions: none
#                     Signature : ecdsa-with-SHA256
#                                 30:45:02:20:01:25:4D:84:D8...
#                 Signed Certificate Timestamp:
#                     Version   : v1 (0x0)
#                     Log ID    : 48:B0:E3:6B:DA...
#                     Timestamp : Jul  8 16:18:08.988 2024 GMT
#                     Extensions: none
#                     Signature : ecdsa-with-SHA256
#                                 48:B0:E3:6B:DA...
#     Signature Algorithm: sha256WithRSAEncryption
#     Signature Value:
#         48:B0:E3:6B:DA...
```


## Resources
- https://datatracker.ietf.org/doc/html/rfc8555/