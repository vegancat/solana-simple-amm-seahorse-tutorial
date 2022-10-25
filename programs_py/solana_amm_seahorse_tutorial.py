# solana_amm_seahorse_tutorial
# Built with Seahorse v0.2.2

from seahorse.prelude import *

declare_id('Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS')

class PoolAccount(Account):
  # in format of tokenX-tokenY 
  ticket: str
  token_a_account: TokenAccount
  token_b_account: TokenAccount
  token_a_amount: u32
  token_b_amount: u32
  fee: u16

@instruction
def create_lp_token():
  pass

@instruction
def initialize_and_provide_liquidity_first(
    initializer: Signer, 
    token_a_mint: TokenMint,
    token_b_mint: TokenMint,
    pool_account: Empty[PoolAccount],
    pool_token_a_account: Empty[TokenAccount],
    pool_token_b_account: Empty[TokenAccount],
    initializer_deposit_token_a_account : TokenAccount,
    initializer_deposit_token_b_account : TokenAccount,
    token_a_deposit_amount: u32,
    token_b_deposit_amount: u32,
    pool_ticket: str,
    # fees in basis points. 10000 = 100%
    pool_fee: u16
  ):
  
  # checking for authority over creating new pools
  # TODO: use keys_eq() instead when it's available
  # TODO: normal equation checking is rather expensive in terms of compute units
  assert initializer.key() == "73BHpXyPbWX1rEBTPKMjDB2aVzZop267iwEBDsoPAE3Q", "Only the admin can create new pools"

  # init a pool
  pool_account.init(
    payer = initializer,
    seeds = [token_a_mint, token_b_mint],
  )

  pool_token_a_account.init(
    payer = initializer,
    seeds = [pool_account, token_a_mint]
  )
  pool_token_b_account.init(
    payer = initializer,
    seeds = [pool_account, token_b_mint]
  )

  assert initializer_deposit_token_a_account.amount >= token_a_deposit_amount, 'In-sufficient balance'
  assert initializer_deposit_token_b_account.amount >= token_b_deposit_amount, 'In-sufficient balance'
  
  pool_account.ticket = pool_ticket
  pool_account.token_a_account = pool_token_a_account
  pool_account.token_b_account = pool_token_b_account
  pool_account.pool_fee = pool_fee


  # these two token transfers would determine the pool ratio
  initializer_deposit_token_a_account.transfer(
    authority=initializer,
    to=pool_token_a_account,
    amount=token_a_deposit_amount
  )

  initializer_deposit_token_b_account.transfer(
    authority=initializer,
    to=pool_token_b_account,
    amount=token_b_deposit_amount
  )

  pool_account.token_a_amount = token_a_deposit_amount
  pool_account.token_b_amount = token_b_deposit_amount


@instruction
def provide_liquidity_additional():
  pass


@instruction
def withdraw_liquidity():
  pass

@instruction
def swap():
  pass
