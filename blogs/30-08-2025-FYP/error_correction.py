from ldpc import bplsd_decoder
from ldpc.codes import rep_code

def _start_error_correction(self, partner_id, sifted_key): 
    H = rep_code(N_BITS)
    key_block = np.array(self._pad_or_truncate_key(sifted_key, N_BITS))
    
    syndrome = (H @ key_block) % 2
    syndrome_str = "".join(str(int(b)) for b in syndrome)
    
    self.sio.emit('announce_syndrome', {'partner_id': partner_id, 'syndrome': syndrome_str})
    self.sifting_info[partner_id]['final_key'] = "".join(map(str, key_block))
    
def correct_key_with_syndrome(self, partner_id, received_syndrome): 
    self._log(f"Received syndrome from {partner_id[:8]}. Correcting my key.")
    info = self.sifting_info.get(partner_id)
    if not info or not info.get('sifted_key'): 
        return
    
    try:
        H = rep_code(N_BITS)
        recv_syndrome = np.array([int(c) for c in received_syndrome], dtype=np.uint8)
        
        # Simulate real-world QBER on the receiver side
        key_with_error = self.introduce_qber_errors(info['sifted_key'], QBER)
        my_key_block = np.array(self._pad_or_truncate_key(key_with_error, N_BITS))
        
        my_syndrome = (H @ my_key_block) % 2
        syndrome_diff = (recv_syndrome - my_syndrome) % 2
        
        decoder = bplsd_decoder.BpLsdDecoder(H, error_rate=QBER, max_iter=100)
        estimated_error = decoder.decode(syndrome_diff) 
        
        estimated_error_rate = int(np.count_nonzero(estimated_error)) / N_BITS
        self._log(f"Estimated QBER with {partner_id[:8]} is {estimated_error_rate:.2%}.")
        
        if estimated_error_rate > QBER_THRESHOLD:
            self._log(f"QBER exceeds threshold! Requesting retry.", is_error=True)
            self.sifting_info[partner_id]['final_key'] = "RETRYING"
            self.sio.emit('qkd_retry_request', {'partner_id': partner_id})
            return
        
        final_key_arr = (my_key_block ^ estimated_error) % 2
        final_key = "".join(map(str, final_key_arr.tolist()))
        
        self._log(f"Error correction successful. Final key established.")
        self.sifting_info[partner_id]['final_key'] = final_key
        self.sio.emit('pair_key_complete', {'partner_id': partner_id})
        
    except Exception as e:
        self._log(f"CRITICAL ERROR during LDPC decoding: {e}\n{traceback.format_exc()}", is_error=True)