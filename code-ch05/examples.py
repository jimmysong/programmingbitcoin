"""
# tag::example1[]
>>> from io import BytesIO
>>> from script import Script  # <1>
>>> script_hex = ('6b483045022100ed81ff192e75a3fd2304004dcadb74' +
...     '6fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb3' +
...     '5d446a89d3f56100f4d7f67801c31967743a9c8e10615bed012103' +
...     '49fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213' +
...     'bf016b278a')
>>> stream = BytesIO(bytes.fromhex(script_hex))
>>> script_sig = Script.parse(stream)
>>> print(script_sig)
3045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01 0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a 

# end::example1[]
"""
