import * as anchor from "@project-serum/anchor";
import { Program } from "@project-serum/anchor";
import { SolanaAmmSeahorseTutorial } from "../target/types/solana_amm_seahorse_tutorial";

describe("solana_amm_seahorse_tutorial", () => {
  // Configure the client to use the local cluster.
  anchor.setProvider(anchor.AnchorProvider.env());

  const program = anchor.workspace.SolanaAmmSeahorseTutorial as Program<SolanaAmmSeahorseTutorial>;

  it("Is initialized!", async () => {
    // Add your test here.
    const tx = await program.methods.initialize().rpc();
    console.log("Your transaction signature", tx);
  });
});
