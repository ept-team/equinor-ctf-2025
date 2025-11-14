# Writeup: FlagPrinter
**Author:** Seppuku_FF1+4 (SamiFF1+4)  
**Team:** Sjokoladepålegg  
**Category:** Reversing

## SpoilerFreeSummary
The binary presents itself as a “secure flag printer” using an encoding routine to protect the flag.
However, a closer look at encoding behavior reveals the reason for its simple retrieval method.

---

## Quick Strings Check
A quick `strings flagprinter | grep EPT` reveals our goal:

![Strings Flagprinter](img_strings.png)

I have to admit I immediately thought this was a fake flag to throw us off for a moment. Always submit it anyway.

## Encoding Behavior Check With GDB

The output already contains a flag, meaning it's hardcoded in the binary.
Just for old time’s sake, we inspect program memory during execution with GDB.

Since the program encodes the flag before printing it, the plaintext must exist right before the encoding routine is applied.  
We break at the start of `encode()` and inspect the first function argument (`rdi`), which is the correct register for x86-64 binaries.  
The `file` command confirms the binary is x86-64.

![GDB Check](img_gdb.png)

GDB resolves the address to the `<FLAG>` symbol, meaning the flag is stored as a static global variable inside the program’s `.data` section.
