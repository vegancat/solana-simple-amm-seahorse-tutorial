#![allow(unused_imports)]
#![allow(unused_variables)]
#![allow(unused_mut)]
use crate::{assign, index_assign, seahorse_util::*};
use anchor_lang::{prelude::*, solana_program};
use anchor_spl::token::{self, Mint, Token, TokenAccount};
use std::{cell::RefCell, rc::Rc};

#[account]
#[derive(Debug)]
pub struct PoolAccount {
    pub ticket: String,
    pub token_a_mint: Pubkey,
    pub token_b_mint: Pubkey,
    pub token_a_amount: u32,
    pub token_b_amount: u32,
    pub fee: u16,
}

impl<'info, 'entrypoint> PoolAccount {
    pub fn load(
        account: &'entrypoint mut Box<Account<'info, Self>>,
        programs_map: &'entrypoint ProgramsMap<'info>,
    ) -> Mutable<LoadedPoolAccount<'info, 'entrypoint>> {
        let ticket = account.ticket.clone();
        let token_a_mint = account.token_a_mint.clone();
        let token_b_mint = account.token_b_mint.clone();
        let token_a_amount = account.token_a_amount;
        let token_b_amount = account.token_b_amount;
        let fee = account.fee;

        Mutable::new(LoadedPoolAccount {
            __account__: account,
            __programs__: programs_map,
            ticket,
            token_a_mint,
            token_b_mint,
            token_a_amount,
            token_b_amount,
            fee,
        })
    }

    pub fn store(loaded: Mutable<LoadedPoolAccount>) {
        let mut loaded = loaded.borrow_mut();
        let ticket = loaded.ticket.clone();

        loaded.__account__.ticket = ticket;

        let token_a_mint = loaded.token_a_mint.clone();

        loaded.__account__.token_a_mint = token_a_mint;

        let token_b_mint = loaded.token_b_mint.clone();

        loaded.__account__.token_b_mint = token_b_mint;

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
    pub token_a_mint: Pubkey,
    pub token_b_mint: Pubkey,
    pub token_a_amount: u32,
    pub token_b_amount: u32,
    pub fee: u16,
}
