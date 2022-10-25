#![allow(unused_imports)]
#![allow(unused_variables)]
#![allow(unused_mut)]
use crate::{assign, index_assign, seahorse_util::*};
use anchor_lang::{prelude::*, solana_program};
use anchor_spl::token::{self, Mint, Token, TokenAccount};
use std::{cell::RefCell, rc::Rc};

#[account]
#[derive(Debug)]
pub struct PoolLiquidityTokenAuthority {
    pub lp_token_supply: u64,
}

impl<'info, 'entrypoint> PoolLiquidityTokenAuthority {
    pub fn load(
        account: &'entrypoint mut Box<Account<'info, Self>>,
        programs_map: &'entrypoint ProgramsMap<'info>,
    ) -> Mutable<LoadedPoolLiquidityTokenAuthority<'info, 'entrypoint>> {
        let lp_token_supply = account.lp_token_supply;

        Mutable::new(LoadedPoolLiquidityTokenAuthority {
            __account__: account,
            __programs__: programs_map,
            lp_token_supply,
        })
    }

    pub fn store(loaded: Mutable<LoadedPoolLiquidityTokenAuthority>) {
        let mut loaded = loaded.borrow_mut();
        let lp_token_supply = loaded.lp_token_supply;

        loaded.__account__.lp_token_supply = lp_token_supply;
    }
}

#[derive(Debug)]
pub struct LoadedPoolLiquidityTokenAuthority<'info, 'entrypoint> {
    pub __account__: &'entrypoint mut Box<Account<'info, PoolLiquidityTokenAuthority>>,
    pub __programs__: &'entrypoint ProgramsMap<'info>,
    pub lp_token_supply: u64,
}

#[account]
#[derive(Debug)]
pub struct PoolAccount {
    pub ticket: String,
    pub token_a_account: SeahorseAccount<'info, '_, TokenAccount>,
    pub token_b_account: SeahorseAccount<'info, '_, TokenAccount>,
    pub token_lp_amount_minted: u64,
    pub token_a_amount: u64,
    pub token_b_amount: u64,
    pub fee: u16,
}

impl<'info, 'entrypoint> PoolAccount {
    pub fn load(
        account: &'entrypoint mut Box<Account<'info, Self>>,
        programs_map: &'entrypoint ProgramsMap<'info>,
    ) -> Mutable<LoadedPoolAccount<'info, 'entrypoint>> {
        let ticket = account.ticket.clone();
        let token_a_account = account.token_a_account.clone();
        let token_b_account = account.token_b_account.clone();
        let token_lp_amount_minted = account.token_lp_amount_minted;
        let token_a_amount = account.token_a_amount;
        let token_b_amount = account.token_b_amount;
        let fee = account.fee;

        Mutable::new(LoadedPoolAccount {
            __account__: account,
            __programs__: programs_map,
            ticket,
            token_a_account,
            token_b_account,
            token_lp_amount_minted,
            token_a_amount,
            token_b_amount,
            fee,
        })
    }

    pub fn store(loaded: Mutable<LoadedPoolAccount>) {
        let mut loaded = loaded.borrow_mut();
        let ticket = loaded.ticket.clone();

        loaded.__account__.ticket = ticket;

        let token_a_account = loaded.token_a_account.clone();

        loaded.__account__.token_a_account = token_a_account;

        let token_b_account = loaded.token_b_account.clone();

        loaded.__account__.token_b_account = token_b_account;

        let token_lp_amount_minted = loaded.token_lp_amount_minted;

        loaded.__account__.token_lp_amount_minted = token_lp_amount_minted;

        let token_a_amount = loaded.token_a_amount;

        loaded.__account__.token_a_amount = token_a_amount;

        let token_b_amount = loaded.token_b_amount;

        loaded.__account__.token_b_amount = token_b_amount;

        let fee = loaded.fee;

        loaded.__account__.fee = fee;
    }
}

#[derive(Debug)]
pub struct LoadedPoolAccount<'info, 'entrypoint> {
    pub __account__: &'entrypoint mut Box<Account<'info, PoolAccount>>,
    pub __programs__: &'entrypoint ProgramsMap<'info>,
    pub ticket: String,
    pub token_a_account: SeahorseAccount<'info, '_, TokenAccount>,
    pub token_b_account: SeahorseAccount<'info, '_, TokenAccount>,
    pub token_lp_amount_minted: u64,
    pub token_a_amount: u64,
    pub token_b_amount: u64,
    pub fee: u16,
}

pub fn init_amm_handler<'info>(
    mut initializer: SeahorseAccount<'info, '_, TokenAccount>,
    mut pool_liquidity_lp_token_authority: Empty<
        Mutable<LoadedPoolLiquidityTokenAuthority<'info, '_>>,
    >,
    mut lp_mint: Empty<SeahorseAccount<'info, '_, Mint>>,
) -> () {
    let mut init_pool_liquidity_lp_token_authority =
        pool_liquidity_lp_token_authority.account.clone();

    lp_mint.account.clone();

    assign!(
        init_pool_liquidity_lp_token_authority
            .borrow_mut()
            .lp_token_supply,
        <u64 as TryFrom<_>>::try_from(0).unwrap()
    );
}
