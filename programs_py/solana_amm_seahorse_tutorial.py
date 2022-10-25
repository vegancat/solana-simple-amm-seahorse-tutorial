# solana_amm_seahorse_tutorial
# Built with Seahorse v0.2.2

from seahorse.prelude import *

declare_id('Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS')

class PoolAccount(Account):
  # in format of tokenX-tokenY 
  ticket: str
  token_a_mint: Pubkey
  token_b_mint: Pubkey
  token_a_amount: u32
  token_b_amount: u32
  fee: u16
