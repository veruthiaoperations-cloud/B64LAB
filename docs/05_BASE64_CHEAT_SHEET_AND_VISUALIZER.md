# Base64 Complete Schema Cheat Sheet & Step-by-Step Visualizer

> **The Definitive Visual Reference Grid & Worked Step-by-Step Examples**  
> *Everything you need to calculate, decode, and visually trace Base64 by hand.*

---

## 1. The Complete 64-Character Schema Lookup Grid

Base64 maps **6-bit binary numbers** (decimal values $0$ through $63$) to printable ASCII characters.

Below is the complete 64-character lookup specification (RFC 4648 Section 4 & Section 5):

| Dec | 6-Bit Binary | Standard Char | URL-Safe Char | | Dec | 6-Bit Binary | Standard Char | URL-Safe Char |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | `000000` | **A** | **A** | | **32** | `100000` | **g** | **g** |
| **1** | `000001` | **B** | **B** | | **33** | `100001` | **h** | **h** |
| **2** | `000010` | **C** | **C** | | **34** | `100010` | **i** | **i** |
| **3** | `000011` | **D** | **D** | | **35** | `100011` | **j** | **j** |
| **4** | `000100` | **E** | **E** | | **36** | `100100` | **k** | **k** |
| **5** | `000101` | **F** | **F** | | **37** | `100101` | **l** | **l** |
| **6** | `000110` | **G** | **G** | | **38** | `100110` | **m** | **m** |
| **7** | `000111` | **H** | **H** | | **39** | `100111` | **n** | **n** |
| **8** | `001000` | **I** | **I** | | **40** | `101000` | **o** | **o** |
| **9** | `001001` | **J** | **J** | | **41** | `101001` | **p** | **p** |
| **10** | `001010` | **K** | **K** | | **42** | `101010` | **q** | **q** |
| **11** | `001011` | **L** | **L** | | **43** | `101011` | **r** | **r** |
| **12** | `001100` | **M** | **M** | | **44** | `101100` | **s** | **s** |
| **13** | `001101` | **N** | **N** | | **45** | `101101` | **t** | **t** |
| **14** | `001110` | **O** | **O** | | **46** | `101110` | **u** | **u** |
| **15** | `001111` | **P** | **P** | | **47** | `101111` | **v** | **v** |
| **16** | `010000` | **Q** | **Q** | | **48** | `110000` | **w** | **w** |
| **17** | `010001` | **R** | **R** | | **49** | `110001` | **x** | **x** |
| **18** | `010010` | **S** | **S** | | **50** | `110010` | **y** | **y** |
| **19** | `010011` | **T** | **T** | | **51** | `110011` | **z** | **z** |
| **20** | `010100` | **U** | **U** | | **52** | `110100` | **0** | **0** |
| **21** | `010101` | **V** | **V** | | **53** | `110101` | **1** | **1** |
| **22** | `010110` | **W** | **W** | | **54** | `110110` | **2** | **2** |
| **23** | `010111` | **X** | **X** | | **55** | `110111` | **3** | **3** |
| **24** | `011000` | **Y** | **Y** | | **56** | `111000` | **4** | **4** |
| **25** | `011001` | **Z** | **Z** | | **57** | `111001` | **5** | **5** |
| **26** | `011010` | **a** | **a** | | **58** | `111010` | **6** | **6** |
| **27** | `011011` | **b** | **b** | | **59** | `111011` | **7** | **7** |
| **28** | `011100` | **c** | **c** | | **60** | `111100` | **8** | **8** |
| **29** | `011101` | **d** | **d** | | **61** | `111101` | **9** | **9** |
| **30** | `011110` | **e** | **e** | | **62** | `111110` | **+** | **-** *(Dash)* |
| **31** | `011111` | **f** | **f** | | **63** | `111111` | **/** | **_** *(Underscore)* |

> **Key Difference for Web Security (Base64URL):**  
> Index **62** becomes `-` (dash) instead of `+`.  
> Index **63** becomes `_` (underscore) instead of `/`.  
> Padding `=` is generally omitted in URLs and JWT tokens.

---

## 2. Step-by-Step Worked Example: Encoding `"Hello"`

Let's encode the word `"Hello"` ($5$ characters / $5$ bytes) into Base64 by hand.

### Step 1: Convert Each Character to ASCII and 8-Bit Binary
* `'H'` = ASCII `72` = `01001000`
* `'e'` = ASCII `101` = `01100101`
* `'l'` = ASCII `108` = `01101100`
* `'l'` = ASCII `108` = `01101100`
* `'o'` = ASCII `111` = `01101111`

### Step 2: Process Chunk #1 (First 3 Bytes: `'H'`, `'e'`, `'l'`)

1. **Concatenate the 3 bytes into a single 24-bit stream:**
   ```
   01001000 01100101 01101100
   ```
2. **Regroup into 4 groups of 6 bits each:**
   ```
   [010010]  [000110]  [010110]  [101100]
   ```
3. **Calculate the Decimal Value for each 6-bit chunk:**
   * `010010` = $16 + 2 = \mathbf{18}$
   * `000110` = $4 + 2 = \mathbf{6}$
   * `010110` = $16 + 4 + 2 = \mathbf{22}$
   * `101100` = $32 + 8 + 4 = \mathbf{44}$
4. **Lookup the Characters in the Base64 Table:**
   * Index 18 $\rightarrow$ **`S`**
   * Index 6  $\rightarrow$ **`G`**
   * Index 22 $\rightarrow$ **`V`**
   * Index 44 $\rightarrow$ **`s`**
   * **Chunk 1 Result:** `"SGVz"`

---

### Step 3: Process Chunk #2 (Remaining 2 Bytes: `'l'`, `'o'`)

1. **Concatenate the 2 bytes (16 bits):**
   ```
   01101100 01101111
   ```
2. **Pad with 2 zero bits on the right to complete three 6-bit groups (18 bits total):**
   ```
   01101100 01101111 00
   ```
3. **Regroup into 6-bit chunks:**
   ```
   [011011]  [000110]  [111100]
   ```
4. **Calculate Decimal Values:**
   * `011011` = $16 + 8 + 2 + 1 = \mathbf{27}$
   * `000110` = $4 + 2 = \mathbf{6}$
   * `111100` = $32 + 16 + 8 + 4 = \mathbf{60}$
5. **Lookup the Characters:**
   * Index 27 $\rightarrow$ **`b`**
   * Index 6  $\rightarrow$ **`G`**
   * Index 60 $\rightarrow$ **`8`**
6. **Append Padding Character (`=`):**
   * Because we had 2 remaining bytes (missing 1 byte to make 3), we append **one `=`** to reach a 4-character output block:
   * **Chunk 2 Result:** `"bG8="`

---

### Step 4: Final Assembled String
Combine Chunk 1 + Chunk 2:
$$\mathbf{"SGVz"} + \mathbf{"bG8="} = \mathbf{"SGVsbG8="}$$

---

## 3. Reverse Worked Example: Decoding `"SGVsbG8="`

Let's reverse the process and decode `"SGVsbG8="` back to `"Hello"`.

```
Character:          'S'          'G'          'V'          's'
Table Index:         18           6            22           44
6-bit Binary:     [010010]     [000110]     [010110]     [101100]

Combined 24 bits:  01001000 01100101 01101100
Slice into 8 bits: [01001000]   [01100101]   [01101100]
Decimal ASCII:         72           101          108
ASCII Character:      'H'           'e'          'l'
```

```
Character:          'b'          'G'          '8'          '='
Table Index:         27           6            60       (Padding)
6-bit Binary:     [011011]     [000110]     [111100]     (Ignored)

Combined 18 bits:  01101100 01101111 [00 - discarded padding bits]
Slice into 8 bits: [01101100]   [01101111]
Decimal ASCII:        108           111
ASCII Character:      'l'           'o'
```

Final Decoded String: **`"Hello"`**

---

## 4. The Three Padding Scenarios Visualized

| Input Word | Input Bytes | Remainder ($N \pmod 3$) | 6-Bit Sextets Produced | Padding Appended | Base64 Output |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`"Cat"`** | 3 bytes (24b) | $0$ | 4 sextets | **None** | `Q2F0` |
| **`"Hi"`** | 2 bytes (16b) | $2$ | 3 sextets (+2 zero bits) | **`=`** (1 pad char) | `SGk=` |
| **`"A"`** | 1 byte (8b) | $1$ | 2 sextets (+4 zero bits) | **`==`** (2 pad chars)| `QQ==` |

---

## 5. Visual Summary Chart

```
RAW BYTES (8 bits each)      [ Byte 1 ]       [ Byte 2 ]       [ Byte 3 ]
BIT STREAM                   1 2 3 4 5 6 7 8  1 2 3 4 5 6 7 8  1 2 3 4 5 6 7 8
                             ───────────┬───  ───────┬───────  ───┬───────────
BASE64 SEXTETS (6 bits each) [ Sextet 1 ]     [ Sextet 2 ]     [ Sextet 3 ]     [ Sextet 4 ]
```
