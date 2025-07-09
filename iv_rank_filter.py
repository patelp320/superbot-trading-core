def is_iv_rank_ok(iv_rank, mode):
    return iv_rank > 50 if mode == 'sell' else iv_rank < 20
