# Beating the kCTF PoW with AVX512IFMA for $51k

> 原文: https://www.ctfiot.com/255114.html
> ID: 255114

Footnotes

$21,337 base reward, $10,000 for stability (successful exploitation on >90% of runs), and $20,000 for a 0-day bug. ↩

We had one shot at this; William’s thesis was due in a few days and we wanted to include the exploit. ↩

Compare with proofs of work, for example, that request a SHA hash starting with some number of zeros. This process is embarrassingly parallel, so someone with many powerful GPUs could solve it in a fraction of the time as someone without. ↩

The Rust implementation uses the exact same Mersenne trick, yet takes about 2.4 seconds; I assume this is FFI overhead? 🤷 ↩

Edit (June 3): Out of curiosity I just tried FLINT—another well-optimized arbitrary-precision library—but found that it was about the same speed as GMP. ↩

Limbs are the term of art for the integer elements of an array that represents a big integer. On 64-bit systems, limbs are usually 64-bit unsigned integers. ↩

See uops.info, imul r64 and mulx r64, r64, r64. ↩

The same performance problem was observed by y-cruncher author Alexander Yee here, section “Example 2: Everything Blows Up”. ↩


```
def sloth_root(x, difficulty=7337):
 for i in range(difficulty): # repeat the inner kernel this many times
 for j in range(1277): # square x this many times
 x = (x * x) % (2 ** 1279 - 1) # modulus is a Mersenne number
 x = x.bit_flip(0) # complement the LSB of x
 return int(x)
```



```
def mod_2_1279_minus_1(x): # compute x % (2 ** 1279 - 1)
 p = 2 ** 1279 - 1
 r = (x & p) + (x >> 1279)
 if r >= p:
 r -= p
 return r
```



```
constexpr int MERSENNE_EXP = 1279;

mpz_t low, high, p;

void mpz_mod_mersenne(mpz_t r, const mpz_t x) {
 // p = 2^n - 1
 mpz_mod_2exp(low, x, MERSENNE_EXP);
 mpz_fdiv_q_2exp(high, x, MERSENNE_EXP);
 mpz_add(r, low, high);
 if (mpz_cmp(r, p) >= 0) {
 mpz_sub(r, r, p);
 }
}

bool init() {
 mpz_inits(low, high, p, NULL);
 mpz_ui_pow_ui(p, 2, MERSENNE_EXP);
 mpz_sub_ui(p, p, 1);
 return true;
}
bool _unused = init();

void the_powmod(mpz_t x) {
 for (int i = 0; i < 1277; ++i) {
 mpz_mul(x, x, x);
 mpz_mod_mersenne(x, x);
 }
}

int main()
{
 const int diff = 7337;
 mpz_t x, r;
 mpz_inits(x, r, NULL);
 mpz_set_str(x, "96729140485950483920373592475530255430", 10);
 for (int i = 0; i < diff; ++i) {
 the_powmod(x);
 mpz_combit(x, 0);
 }
 char *str = mpz_get_str(NULL, 10, x);
 std::cout << "x: " << str << std::endl;
 return 0;
}
```



```
// vpmadd52luq dst, a, b
void vpmadd52luq(uint64_t dst[8], uint64_t a[8], uint64_t b[8]) {
 for (int i = 0; i < 8; ++i) {
 dst[i] += (a[i] * b[i]) & (1ULL << 52 - 1);
 }
}

// vpmadd52huq dst, a, b
void vpmadd52huq(uint64_t dst[8], uint64_t a[8], uint64_t b[8]) {
 for (int i = 0; i < 8; ++i) {
 dst[i] += ((__uint128_t)a[i] * b[i]) >> 52;
 }
}
```



```
// Computing the second term
// input contains the 25 52-bit limbs, stored in 64-bit words
_Alignas(64) uint64_t padded_data[8 * 6] = {0}; // so that loads OOB are still valid
uint64_t *data = padded_data + 8;

__m512i clumps[4] = {
 _mm512_loadu_si512(input),
 _mm512_loadu_si512(input + 8),
 _mm512_loadu_si512(input + 16),
 _mm512_loadu_si512(input + 24)
};

_mm512_store_si512(data, clumps[0]);
_mm512_store_si512(data + 8, clumps[1]);
_mm512_store_si512(data + 16, clumps[2]);
_mm512_store_si512(data + 24, clumps[3]);

#define ZERO _mm512_setzero_si512()

// Seven zmm accumulators are necessary
__m512i accum[7] = { ZERO /* 0-7 */, ZERO /* 8-15, etc. */, ZERO, ZERO, ZERO, ZERO, ZERO };
for (int i = -7; i <= 24; ++i) {
 // Sliding window
 __m512i m1 = _mm512_loadu_si512(data + i); // Load the current window of 8 elements
 for (int j = 0, k = 0; j < 7; ++j, k += 8) {
 // Decide whether to accumulate into accum[j], which should happen if there
 // is at least one element shared between the jth accumulator and [i, i+7]
 int lo = k - i;
 int hi = k - i - 1;
 // Process low halves
 if (lo >= 0 && lo <= 24) {
 // Discard out of bounds multiplications
 __mmask8 sel = (uint8_t)(lo < i ? -1ULL : (-1ULL << (lo - i + 1)));
 if (sel) {
 accum[j] = _mm512_mask_madd52lo_epu64(accum[j], sel, m1, _mm512_set1_epi64(data[lo]));
 }
 }
 // Process high halves
 if (hi >= 0 && hi <= 24) {
 // ditto
 __mmask8 sel = (uint8_t)(hi < i ? -1ULL : (-1ULL << (hi - i + 1)));
 if (sel) {
 accum[j] = _mm512_mask_madd52hi_epu64(accum[j], sel, m1, _mm512_set1_epi64(data[hi]));
 }
 }
 }
}
```



```
Accumulating low halves: window 1 by limb 7 with mask 10000000
Accumulating high halves: window 1 by limb 6 with mask 11000000
Accumulating low halves: window 2 by limb 6 with mask 11100000
Accumulating high halves: window 2 by limb 5 with mask 11110000
Accumulating low halves: window 3 by limb 5 with mask 11111000
Accumulating high halves: window 3 by limb 4 with mask 11111100
Accumulating low halves: window 4 by limb 4 with mask 11111110
Accumulating high halves: window 4 by limb 3 with mask 11111111
Accumulating low halves: window 5 by limb 3 with mask 11111111
Accumulating high halves: window 5 by limb 2 with mask 11111111
Accumulating low halves: window 6 by limb 2 with mask 11111111
Accumulating high halves: window 6 by limb 1 with mask 11111111
Accumulating low halves: window 7 by limb 1 with mask 11111111
Accumulating high halves: window 7 by limb 0 with mask 11111111
Accumulating low halves: window 8 by limb 0 with mask 11111111
```



```
for (int i = 0; i < 4; ++i) {
 __m512d diag_lo = _mm512_castsi512_pd(_mm512_madd52lo_epu64(ZERO, clumps[i], clumps[i]));
 __m512d diag_hi = _mm512_castsi512_pd(_mm512_madd52hi_epu64(ZERO, clumps[i], clumps[i]));
 __m512i shuf_lo = _mm512_set_epi64(11, 3, 10, 2, 9, 1, 8, 0);
 __m512i shuf_hi = _mm512_set_epi64(15, 7, 14, 6, 13, 5, 12, 4);
 accum[2 * i] = _mm512_add_epi64(accum[2*i], _mm512_castpd_si512(_mm512_permutex2var_pd(diag_lo, shuf_lo, diag_hi)));
 if (i != 3) {
 accum[2 * i + 1] = _mm512_add_epi64(accum[2*i+1], _mm512_castpd_si512(_mm512_permutex2var_pd(diag_lo, shuf_hi, diag_hi)));
 }
}
```



```
__m512i low_52_bits = _mm512_set1_epi64((1ULL << 52) - 1);
__m512i hi_12_bits = _mm512_set1_epi64(~((1ULL << 52) - 1));

__m512i high_1279[4];
shift_down_1279(accum, high_1279);
filter_low_1279(accum);

for (int i = 0; i < 4; ++i) {
 accum[i] = _mm512_add_epi64(accum[i], high_1279[i]);
}

{
carry2:;
__m512i carry_test = _mm512_setzero_si512();
__m512i group_out = _mm512_setzero_si512();
for (int i = 0; i < 4; ++i) {
 __m512i carries = _mm512_srli_epi64(accum[i], 52);
 __m512i carries_into = _mm512_alignr_epi64(carries, group_out, 7);
 accum[i] = _mm512_add_epi64(_mm512_and_si512(accum[i], low_52_bits), carries_into);
 group_out = carries;
 carry_test = _mm512_and_si512(carry_test, accum[i]); // improve latency over a series of masked tests
}

if (__builtin_expect(_mm512_test_epi64_mask(carry_test, hi_12_bits), 0)) {
 goto carry2;
}
}
```



```
// Now compare with 2^1279 - 1; if >=, subtract 2^1279 - 1. classic Mersenne number modulo algorithm
__m512i bit_1279 = _mm512_set_epi64(0, 0, 0, 0, 0, 0, 0, 1ULL << 31);
__m512i mask_off = _mm512_set_epi64(0, 0, 0, 0, 0, 0, 0, (1ULL << 31) - 1);

// Branchless approach appears to save about 2 ns per iteration. Also, we stay in vector regs and don't use a test mask here because it tends to be slower
__m512i cmp = _mm512_and_epi64(accum[3], bit_1279);
accum[0] = _mm512_add_epi64(accum[0], _mm512_srli_epi64(cmp, 31)); // potentially +1 to last word
accum[3] = _mm512_and_si512(mask_off, accum[3]);

// TODO 1/2^52 chance of error here due to carry -- check it
```



```
__m512i accum[7] = { ZERO /* 0-7 */, ZERO /* 8-15, etc. */, ZERO, ZERO, ZERO, ZERO, ZERO };
__m512i accum_hi[7] = { ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO };

// ... fmadd spam goes here ...

// Fold high and low halves
for (int i = 0; i < 7; ++i) {
 accum[i] = _mm512_add_epi64(accum[i], accum_hi[i]);
}
```



```
if (lo >= 0 && lo <= 24) {
 // Multiples of 8 are handled by a register broadcast instead of a memory load for efficiency
#define FOR_EACH_OFFS X(1) X(2) X(3) X(4) X(5) X(6) X(7) X(9) X(10) X(11) X(12) X(13) X(14) X(15) X(17) X(18) X(19) X(20) X(21) X(22) X(23)
 __mmask8 sel = (uint8_t)(lo < i ? -1ULL : (-1ULL << (lo - i + 1)));
 if (sel == (uint8_t)-1 && ELIDE_MASKS_IF_POSSIBLE) {
#define X(n) case n: asm volatile ("vpmadd52luq %0, %1, %2%{1to8%}" : "+v"(accum[j]) : "v"(m1), "m"(data[n])); break;
 switch (lo) {
 FOR_EACH_OFFS
 default:
 accum[j] = _mm512_madd52lo_epu64(accum[j], m1, _mm512_broadcast_i32x2(_mm512_castsi512_si128(clumps[lo/ 8])));
 }

 } else if (sel) {
#define X(n) case n: asm volatile ("vpmadd52luq %0 %{%1%}, %2, %3%{1to8%}" : "+v"(accum[j]) : "Yk"(sel), "v"(m1), "m"(data[n])); break;
 switch (lo) {
 FOR_EACH_OFFS
 default:
 accum[j] = _mm512_mask_madd52lo_epu64(accum[j], sel, m1, _mm512_broadcast_i32x2(_mm512_castsi512_si128(clumps[lo/8])));
 }
 }
}
```



```
__m512i m1;
if ((i & 7) == 0) {
 m1 = clumps[i / 8];
} else {
#define UNALIGNED(S) case S: { m1 = _mm512_alignr_epi64(clumps[(i+8)/8], i < 0 ? _mm512_setzero_si512() : clumps[(i+8)/8-1], S); break; }
 switch (i & 7) {
 UNALIGNED(1)
 UNALIGNED(2)
 UNALIGNED(3)
 UNALIGNED(4)
 UNALIGNED(5)
 UNALIGNED(6)
 UNALIGNED(7)
 default: abort();
 }
}
```



```
// Written by Timothy Herchen
// gcc main.c -O3 -march=znver5 -masm=intel -lgmp
#include <immintrin.h>
#include <gmp.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>

#define uint128_t __uint128_t

void gmp_to_array(mpz_t mpz, uint64_t *array) {
 size_t N;
 mpz_export(array, &N, 1, sizeof(uint64_t), 0, 0, mpz);
 for (int i = 0, j = N - 1; i < j; ++i, --j) {
 uint64_t temp = array[i];
 array[i] = array[j];
 array[j] = temp;
 }
}

// Destroys the array
void array_to_gmp(uint64_t *array, mpz_t mpz, uint64_t words) {
 for (int i = 0, j = words - 1; i < j; ++i, --j) {
 uint64_t temp = array[i];
 array[i] = array[j];
 array[j] = temp;
 }
 mpz_import(mpz, words, 1, sizeof(uint64_t), 0, 0, array);
}

size_t convert_radix_64_to_52(uint64_t *limbs, uint64_t *out, size_t count) {
 size_t out_index = 0;
 int bits_in_buffer = 0;
 uint128_t buffer = 0;

 for (size_t i = 0; i < count; i++) {
 buffer |= ((uint128_t)limbs[i]) << bits_in_buffer;
 bits_in_buffer += 64;

 while (bits_in_buffer >= 52) {
 out[out_index++] = (uint64_t)(buffer & ((1ULL << 52) - 1));
 buffer >>= 52;
 bits_in_buffer -= 52;
 }
 }

 // Handle remaining bits if any
 if (bits_in_buffer > 0) {
 out[out_index++] = (uint64_t)(buffer & ((1ULL << bits_in_buffer) - 1));
 }

 return out_index;
}

size_t convert_radix_52_to_64(uint64_t *in, uint64_t *out, size_t count) {
 size_t out_index = 0;
 int bits_in_buffer = 0;
 uint128_t buffer = 0;

 for (size_t i = 0; i < count; i++) {
 buffer |= ((uint128_t)in[i]) << bits_in_buffer;
 bits_in_buffer += 52;

 while (bits_in_buffer >= 64) {
 out[out_index++] = (uint64_t)(buffer & (((uint128_t)1ULL << 64) - 1));
 buffer >>= 64;
 bits_in_buffer -= 64;
 }
 }

 // Handle remaining bits if any
 if (bits_in_buffer > 0) {
 out[out_index++] = (uint64_t)(buffer & ((1ULL << bits_in_buffer) - 1));
 }

 return out_index;
}

__attribute__((always_inline)) void shift_down_1279(__m512i accum[7], __m512i high_1279[4]) {
	__m512i p = _mm512_setzero_si512();
#pragma GCC unroll 4
	for (int i = 3; i >= 0; --i) {
 __m512i down_31 = _mm512_srli_epi64(accum[i + 3], 31);
 __m512i higher_21 = _mm512_slli_epi64(_mm512_and_si512(accum[i + 3], _mm512_set1_epi64((1ULL << 31) - 1)), 21);
 high_1279[i] = _mm512_add_epi64(_mm512_alignr_epi64(p, higher_21, 1), down_31);
 p = higher_21;
	}
}

__attribute__((always_inline)) void filter_low_1279(__m512i accum[7]) {
	accum[3] = _mm512_and_si512(accum[3], _mm512_set_epi64(0, 0, 0, 0, 0, 0, 0, (1ULL << 31) - 1));
}

// This code is extremely latency bound, as you'd expect for this kind of stupid PoW, so certain things are done that would lower
// throughput (e.g. on a hyperthreaded device doing two of these at once) but which lower the latency
void the_powmod(uint64_t * __restrict__ input, uint64_t * __restrict__ result) {
	_Alignas(64) uint64_t padded_data[8 * 6] = {0};
	uint64_t *data = padded_data + 8;

	__m512i clumps[4] = {
 _mm512_loadu_si512(input),
 _mm512_loadu_si512(input + 8),
 _mm512_loadu_si512(input + 16),
 _mm512_loadu_si512(input + 24)
	};

	for (int pow_i = 0; pow_i < 1277; ++pow_i) {
 // Use aligned stores to make sure we are doing things well
 _mm512_store_si512(data, clumps[0]);
 _mm512_store_si512(data + 8, clumps[1]);
 _mm512_store_si512(data + 16, clumps[2]);
 _mm512_store_si512(data + 24, clumps[3]);

	// Now data[x] gives us the xth limb
#define ZERO _mm512_setzero_si512()

#define ELIDE_MASKS_IF_POSSIBLE 1

	__m512i accum[7] = { ZERO /* 0-7 */, ZERO /* 8-15, etc. */, ZERO, ZERO, ZERO, ZERO, ZERO };
	// The accumulation is latency bound (lat. 4 cycles, so we need at least 8 accumulators to keep the madds in flight)
	__m512i accum_hi[7] = { ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO };
	// We'll laboriously build up the upper triangle of the 2560-bit product using 52x52->104 multiplies
#pragma GCC unroll 100
	for (int i = 24; i >= -7; --i) {
 // Sliding window
 __m512i m1;
 if ((i & 7) == 0) {
 m1 = clumps[i / 8];
 } else {
 // Emulate an unaligned load from memory. Unaligned loads are very expensive on Zen 5 so this is helpful
#define UNALIGNED(S) case S: { m1 = _mm512_alignr_epi64(clumps[(i+8)/8], i < 0 ? _mm512_setzero_si512() : clumps[(i+8)/8-1], S); break; }
 switch (i & 7) {
 UNALIGNED(1)
 UNALIGNED(2)
 UNALIGNED(3)
 UNALIGNED(4)
 UNALIGNED(5)
 UNALIGNED(6)
 UNALIGNED(7)
 default: abort();
 }
 }

#pragma GCC unroll 100
 for (int j = 0, k = 0; j < 7; ++j, k += 8) {
 // Decide whether to accumulate into accum[j], which should happen if there
 // is at least one element shared between the jth accumulator and [i, i+7]
 int lo = k - i;
 int hi = k - i - 1;
 if (lo >= 0 && lo <= 24) {
 // Multiples of 8 are handled by a broadcast instead of a memory load for efficiency
#define FOR_EACH_OFFS X(1) X(2) X(3) X(4) X(5) X(6) X(7) X(9) X(10) X(11) X(12) X(13) X(14) X(15) X(17) X(18) X(19) X(20) X(21) X(22) X(23)
 // Discard those entries where lo > i
 __mmask8 sel = (uint8_t)(lo < i ? -1ULL : (-1ULL << (lo - i + 1)));
 // we use inline asm with a memory broadcast after enough regs because the register allocator does not enjoy this type of setup
 if (sel == (uint8_t)-1 && ELIDE_MASKS_IF_POSSIBLE) {
#define X(n) case n: asm volatile ("vpmadd52luq %0, %1, %2%{1to8%}" : "+v"(accum[j]) : "v"(m1), "m"(data[n])); break;
 switch (lo) {
 FOR_EACH_OFFS
 default:
 accum[j] = _mm512_madd52lo_epu64(accum[j], m1, _mm512_broadcast_i32x2(_mm512_castsi512_si128(clumps[lo/ 8])));
 }

 } else if (sel) {
#define X(n) case n: asm volatile ("vpmadd52luq %0 %{%1%}, %2, %3%{1to8%}" : "+v"(accum[j]) : "Yk"(sel), "v"(m1), "m"(data[n])); break;
 switch (lo) {
 FOR_EACH_OFFS
 default:
 accum[j] = _mm512_mask_madd52lo_epu64(accum[j], sel, m1, _mm512_broadcast_i32x2(_mm512_castsi512_si128(clumps[lo/8])));
 }
 }
 }

 if (hi >= 0 && hi <= 24) {
#undef X
 __mmask8 sel = (uint8_t)(hi < i ? -1ULL : (-1ULL << (hi - i + 1)));
 // see above
 if (sel == (uint8_t)-1 && ELIDE_MASKS_IF_POSSIBLE) {
#define X(n) case n: asm volatile ("vpmadd52huq %0, %1, %2%{1to8%}" : "+v"(accum_hi[j]) : "v"(m1), "m"(data[n])); break;
 switch (hi) {
 FOR_EACH_OFFS
 default:
 accum_hi[j] = _mm512_madd52hi_epu64(accum_hi[j], m1, _mm512_broadcast_i32x2(_mm512_castsi512_si128(clumps[hi / 8])) );
 }
 } else if (sel) {

#define X(n) case n: asm volatile ("vpmadd52huq %0 %{%1%}, %2, %3%{1to8%}" : "+v"(accum_hi[j]) : "Yk"(sel), "v"(m1), "m"(data[n])); break;
 switch (hi) {
 FOR_EACH_OFFS
 default:
 accum_hi[j] = _mm512_mask_madd52hi_epu64(accum_hi[j], sel, m1,_mm512_broadcast_i32x2(_mm512_castsi512_si128(clumps[hi / 8])));
 }
 }
 }

 }
	}

	// Fold high and low halves, and double all the accumulators
#pragma GCC unroll 7
	for (int i = 0; i < 7; ++i) {
 accum[i] = _mm512_add_epi64(accum[i], accum_hi[i]);
 accum[i] = _mm512_add_epi64(accum[i], accum[i]);
	}

	// Now add the diagonal from the accumulators because they weren't yet computed
#pragma GCC unroll 4
	for (int i = 0; i < 4; ++i) {
 __m512d diag_lo = _mm512_castsi512_pd(_mm512_madd52lo_epu64(ZERO, clumps[i], clumps[i]));
 __m512d diag_hi = _mm512_castsi512_pd(_mm512_madd52hi_epu64(ZERO, clumps[i], clumps[i]));
 __m512i shuf_lo = _mm512_set_epi64(11, 3, 10, 2, 9, 1, 8, 0);
 __m512i shuf_hi = _mm512_set_epi64(15, 7, 14, 6, 13, 5, 12, 4);
 accum[2 * i] = _mm512_add_epi64(accum[2*i], _mm512_castpd_si512(_mm512_permutex2var_pd(diag_lo, shuf_lo, diag_hi)));
 if (i != 3) {
 accum[2 * i + 1] = _mm512_add_epi64(accum[2*i+1], _mm512_castpd_si512(_mm512_permutex2var_pd(diag_lo, shuf_hi, diag_hi)));
 }
	}

	// Now propagate carries in parallel in radix 2^52
	__m512i low_52_bits = _mm512_set1_epi64((1ULL << 52) - 1);
	__m512i hi_12_bits = _mm512_set1_epi64(~((1ULL << 52) - 1));

	// Now add the high 1279 bits to the low 1279 bits
	__m512i high_1279[4];
	shift_down_1279(accum, high_1279);
	filter_low_1279(accum);

#pragma GCC unroll 4
	for (int i = 0; i < 4; ++i) {
 accum[i] = _mm512_add_epi64(accum[i], high_1279[i]);
	}

	{
carry2:;
	__m512i carry_test = _mm512_setzero_si512();
	__m512i group_out = _mm512_setzero_si512();
#pragma GCC unroll 7
	for (int i = 0; i < 4; ++i) {
 __m512i carries = _mm512_srli_epi64(accum[i], 52);
 __m512i carries_into = _mm512_alignr_epi64(carries, group_out, 7);
 accum[i] = _mm512_add_epi64(_mm512_and_si512(accum[i], low_52_bits), carries_into);
 group_out = carries;
 carry_test = _mm512_and_si512(carry_test, accum[i]); // improve latency over a series of masked tests
	}

	if (__builtin_expect(_mm512_test_epi64_mask(carry_test, hi_12_bits), 0)) {
 goto carry2;
	}
	}

	// Now compare with 2^1279 - 1; if >=, subtract 2^1279 - 1. classic Mersenne number modulo algorithm
	__m512i bit_1279 = _mm512_set_epi64(0, 0, 0, 0, 0, 0, 0, 1ULL << 31);
	__m512i mask_off = _mm512_set_epi64(0, 0, 0, 0, 0, 0, 0, (1ULL << 31) - 1);

	// Branchless approach appears to save about 2 ns per iteration. Also, we stay in vector regs and don't use a test mask here because it tends to be slower
	__m512i cmp = _mm512_and_epi64(accum[3], bit_1279);
	accum[0] = _mm512_add_epi64(accum[0], _mm512_srli_epi64(cmp, 31)); // potentially +1 to last word
	accum[3] = _mm512_and_si512(mask_off, accum[3]);

	// TODO 1/2^52 chance of error here due to carry -- check it

#pragma GCC unroll 4
	for (int i = 0; i < 4; ++i) {
 clumps[i] = accum[i];
	}
	}

	_mm512_storeu_si512(result, clumps[0]);
	_mm512_storeu_si512(result + 8, clumps[1]);
	_mm512_storeu_si512(result + 16, clumps[2]);
	_mm512_storeu_si512(result + 24, clumps[3]);
}

int main(int argc, char **argv) {
	if (argc < 3) {
 fprintf(stderr, "Usage: %s <y> <difficulty>", argv[0]);
 return 1;
	}

	mpz_t x, r;
	mpz_inits(x, r, NULL);
	mpz_set_str(x, argv[1], 10);
	int difficulty = atoi(argv[2]);

	uint64_t abc[400];
	_Alignas(64) uint64_t poop[32];

	gmp_to_array(x, abc);

	size_t N = convert_radix_64_to_52(abc, poop, 20);

	uint64_t squared[1000];
	for (int i = 0; i < difficulty; ++i) { // specified algorithm
 the_powmod(poop, squared);
 squared[0] ^= 1;
 memcpy(poop, squared, 25 * sizeof(uint64_t));
	}
	convert_radix_52_to_64(squared, abc, 48);
	array_to_gmp(abc, r, 1280/64);

	char *str = mpz_get_str(NULL, 10, r);
	printf("%s", str);
	return 0;
}
```
