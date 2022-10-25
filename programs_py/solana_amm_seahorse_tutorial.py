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

class PoolLiquidityTokenAuthority(Account):
  bump: u8
  # TODO: remove this when there is support for fetching supply of a token in seahorse
  supply: u64

@instruction
def init_amm(
    initializer: TokenAccount, 
    pool_liquidity_lp_token_authority: Empty[PoolLiquidityTokenAuthority], 
    lp_mint: Empty[TokenMint]
  ):
  
  assert initializer.key() == "73BHpXyPbWX1rEBTPKMjDB2aVzZop267iwEBDsoPAE3Q"

  init_pool_liquidity_lp_token_authority = pool_liquidity_lp_token_authority.init(
    payer = initializer,
    seeds = ['pool_liquidity_lp_token_authority']
  )

  lp_mint.init(
    payer = initializer,
    seeds = ['pool_liquidity_lp_token_mint'],
    decimals = 6,
    authority = pool_liquidity_lp_token_authority
  )

  init_pool_liquidity_lp_token_authority.bump = pool_liquidity_lp_token_authority.bump()
  init_pool_liquidity_lp_token_authority.supply = 0
  

@instruction
def initialize_and_provide_liquidity_first(
    initializer: Signer, 
    token_a_mint: TokenMint,
    token_b_mint: TokenMint,
    lp_mint: TokenMint,
    pool_account: Empty[PoolAccount],
    pool_token_a_account: Empty[TokenAccount],
    pool_token_b_account: Empty[TokenAccount],
    pool_liquidity_lp_token_authority: PoolLiquidityTokenAuthority,
    initializer_deposit_token_a_account : TokenAccount,
    initializer_deposit_token_b_account : TokenAccount,
    initializer_receive_lp_token_account: TokenAccount,
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

  # IMPORTANT: this process is simplified for the sake of the tutorial
  # in reality, the amount of LP tokens minted should be calculated based on various factors
  # such as the total supply of LP tokens, the amount of tokens deposited, and the current ratio of the pool
  # calculating the amount of LP tokens to mint
  amount_of_lp_tokens_to_mint = token_a_deposit_amount

  # minting the liquidity tokens
  lp_mint.mint(
    authority = pool_liquidity_lp_token_authority,
    to = initializer_receive_lp_token_account,
    amount = amount_of_lp_tokens_to_mint,
    signer = ['pool_liquidity_lp_token_mint', pool_liquidity_lp_token_authority.bump]
  )

  # updating the supply of the LP token
  pool_liquidity_lp_token_authority.supply += amount_of_lp_tokens_to_mint

@instruction
def provide_liquidity_additional():
  pass


@instruction
def withdraw_liquidity():
  pass

@instruction
def swap():
  pass
