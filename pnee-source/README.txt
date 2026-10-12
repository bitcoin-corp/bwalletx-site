PNEE contracts (sCrypt, scrypt-ts 1.4.5, compiler 1.20.0+commit.693498a)

bondVault.ts.txt  the vault: lock, topUp, mint (up to minRatioPct), close (burn the PNEEs), liquidate (below liqRatioPct)
bondToken.ts.txt  the PNEE token: transfer (amount-conserving), burn

Compiled template fingerprints (md5 of the sCrypt artifact), as fixed in bWalletX:
  BondVault 23ab9141fba782ec2e2bc5aa36ad4f7d
  BondToken ac271b4a048ada099540d58c3d3c24f5

Parameters of the bWalletX deployment (constructor values in every vault script):
  unitCents 1   one PNEE = one cent
  minRatioPct 1000   mint up to 10x
  liqRatioPct 150   anyone may close below 150%
  liqDiscountPct 10   the closer takes the PNEEs plus 10% in BSV
  feeBps 0   no fee
  maxPriceAge 600 s
