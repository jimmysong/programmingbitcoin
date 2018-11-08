from io import BytesIO
from unittest import TestCase

import op
import script

from ecc import S256Point, Signature
from helper import hash160
from op import encode_num
from script import Script


class Chapter6Test(TestCase):

    def test_apply(self):

        def op_hash160(stack):
            if len(stack) < 1:
                return False
            element = stack.pop()
            h160 = hash160(element)
            stack.append(h160)
            return True

        def op_checksig(stack, z):
            if len(stack) < 2:
                return False
            sec_pubkey = stack.pop()
            der_signature = stack.pop()[:-1]
            try:
                point = S256Point.parse(sec_pubkey)
                sig = Signature.parse(der_signature)
            except (ValueError, SyntaxError) as e:
                print(e)
                return False
            if point.verify(z, sig):
                stack.append(encode_num(1))
            else:
                stack.append(encode_num(0))
            return True

        op.op_hash160 = op_hash160
        op.op_checksig = op_checksig
        op.OP_CODE_FUNCTIONS[172] = op_checksig

    def test_example_1(self):
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        sec = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34')
        sig = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab601')
        script_pubkey = Script([sec, 0xac])
        script_sig = Script([sig])
        combined_script = script_sig + script_pubkey
        self.assertEqual(combined_script.evaluate(z), True)

    def test_exercise_3(self):
        hex_script_pubkey = '06767695935687'
        script_pubkey = Script.parse(BytesIO(bytes.fromhex(hex_script_pubkey)))
        hex_script_sig = '0152'
        script_sig = Script.parse(BytesIO(bytes.fromhex(hex_script_sig)))
        combined_script = script_sig + script_pubkey
        self.assertEqual(combined_script.evaluate(0), True)

    def test_exercise_4(self):
        hex_script_pubkey = '086e879169a77ca787'
        script_pubkey = Script.parse(BytesIO(bytes.fromhex(hex_script_pubkey)))
        hex_script_sig = 'fd86024d4001255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe017f46dc93a6b67e013b029aaa1db2560b45ca67d688c7f84b8c4c791fe02b3df614f86db1690901c56b45c1530afedfb76038e972722fe7ad728f0e4904e046c230570fe9d41398abe12ef5bc942be33542a4802d98b5d70f2a332ec37fac3514e74ddc0f2cc1a874cd0c78305a21566461309789606bd0bf3f98cda8044629a14d4001255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe017346dc9166b67e118f029ab621b2560ff9ca67cca8c7f85ba84c79030c2b3de218f86db3a90901d5df45c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d23c570feb141398bb552ef5a0a82be331fea48037b8b5d71f0e332edf93ac3500eb4ddc0decc1a864790c782c76215660dd309791d06bd0af3f98cda4bc4629b1'
        script_sig = Script.parse(BytesIO(bytes.fromhex(hex_script_sig)))
        combined_script = script_sig + script_pubkey
        self.assertEqual(combined_script.evaluate(0), True)        
