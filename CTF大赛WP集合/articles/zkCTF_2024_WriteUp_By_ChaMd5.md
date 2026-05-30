# zkCTF 2024 WriteUp By ChaMd5

> 原文: https://www.ctfiot.com/162396.html
> ID: 162396

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组


```
{"a":"1","b":"1"}
circom checkin.circom --r1cs --wasm --sym -c
node generate_witness.js checkin.wasm input.json witness.wtns
snarkjs groth16 prove ../CheckIn_groth16.zkey witness.wtns proof.json public.json
snarkjs generatecall
["0x2478448102d76d164d4cd8c001ace8a50b2b6232a5ec1801cb7d1f1bf8bae8c1", "0x2fb0bb8d1981019cb9b4abe9fb7d77bf897f89854535614943a14b58d4764cb9"],[["0x1c880a4ecf831386131f976534bfcba6cbb2c30e75715bf721f86b292c83cc91", "0x189ccea3564b26958b6bb4926014c49e73b900c6c79a15246ae802eaa465d106"],["0x01c76d47c68815d508c8bbeb2fa94461cad69b92cf37b20af9a326e274073c9b", "0x21bbdaa303cf72b7b919140e0b913b8e45bfbd590471dd59a36d2f18c5c3fd41"]],["0x255e6500e0c6ec57c17d3aad029ae0bc35abd2831a1656ec0038bb38df8aca51", "0x18d41efa48244bc69577b9dbcdb98ad17c8d538fb076d095e3aacd272ac35b4c"],["0x0000000000000000000000000000000000000000000000000000000000000001"]
use halo2_proofs::
arithmetic::
FieldExt;
use halo2_proofs::{
    arithmetic::
Field,
    circuit::{AssignedCell, Chip, Layouter, Region, SimpleFloorPlanner, Value},
    dev::
MockProver,
    pasta::{EqAffine, Fp},
    plonk::{
        create_proof, keygen_pk, keygen_vk, verify_proof, Advice, Circuit, Column,
        ConstraintSystem, Error, Expression, Fixed, Instance, ProvingKey, Selector, SingleVerifier,
        VerifyingKey,
    },
    poly::{commitment::
Params, Rotation},
    transcript::{Blake2bRead, Blake2bWrite, Challenge255},
};
use serde::{Deserialize, Serialize};
use std::
marker::
PhantomData;
#[derive(Debug, Clone)]
pub struct FibonacciConfig {
    pub col_a: Column<Advice>,
    pub col_b: Column<Advice>,
    pub col_c: Column<Advice>,
    pub col_pa: Column<Fixed>,
    pub col_pb: Column<Fixed>,
    pub col_pc: Column<Fixed>,
    pub selector: Selector,
    pub instance: Column,
}
#[derive(Debug, Clone)]
struct FibonacciChip<F: FieldExt> {
    config: FibonacciConfig,
    _marker: PhantomData<F>,
}
impl<F: FieldExt> FibonacciChip<F> {
    pub fn construct(config: FibonacciConfig) -> Self {
        Self {
            config,
            _marker: PhantomData,
        }
    }
    pub fn configure(meta: &mut ConstraintSystem<F>) -> FibonacciConfig {
        let col_a = meta.advice_column();
        let col_b = meta.advice_column();
        let col_c = meta.advice_column();
        let col_pa = meta.fixed_column();
        let col_pb = meta.fixed_column();
        let col_pc = meta.fixed_column();
        let selector = meta.selector();
        let instance = meta.instance_column();
        meta.enable_equality(col_a);
        meta.enable_equality(col_b);
        meta.enable_equality(col_c);
        meta.enable_equality(instance);
        ///////////////////////// Please implement code here /////////////////////////
        meta.create_gate("add", |meta| {
            //
            // col_a | col_b | col_c | selector
            //   a      b        c       s
            //
            let s = meta.query_selector(selector);
            let a = meta.query_advice(col_a, Rotation::
cur());
            let b = meta.query_advice(col_b, Rotation::
cur());
            let c = meta.query_advice(col_c, Rotation::
cur());
            vec![s * (a + b - c)]
        });
        FibonacciConfig {
            col_a,
            col_b,
            col_c,
            col_pa,
            col_pb,
            col_pc,
            selector,
            instance,
        }
    }
    #[allow(clippy::
type_complexity)]
    pub fn assign_first_row(
        &self,
        mut layouter: impl Layouter<F>,
    ) -> Result<(AssignedCell<F, F>, AssignedCell<F, F>, AssignedCell<F, F>), Error> {
        layouter.assign_region(
            || "first row",
            |mut region| {
                self.config.selector.enable(&mut region, 0)?;
                let a_cell = region.assign_advice_from_instance(
                    || "f(0)",
                    self.config.instance,
                    0,
                    self.config.col_a,
                    0,
                )?;
                let b_cell = region.assign_advice_from_instance(
                    || "f(1)",
                    self.config.instance,
                    1,
                    self.config.col_b,
                    0,
                )?;
                let c_cell = region.assign_advice(
                    || "a + b",
                    self.config.col_c,
                    0,
                    || a_cell.value().copied() + b_cell.value(),
                )?;
                region.assign_fixed(
                    || "pb",
                    self.config.col_pb,
                    0,
                    || Value::
known(F::
from(127)),
                )?;
                Ok((a_cell, b_cell, c_cell))
            },
        )
    }
    pub fn assign_row(
        &self,
        mut layouter: impl Layouter<F>,
        prev_b: &AssignedCell<F, F>,
        prev_c: &AssignedCell<F, F>,
    ) -> Result<AssignedCell<F, F>, Error> {
        layouter.assign_region(
            || "next row",
            |mut region| {
                self.config.selector.enable(&mut region, 0)?;
                prev_b.copy_advice(|| "a", &mut region, self.config.col_a, 0)?;
                prev_c.copy_advice(|| "b", &mut region, self.config.col_b, 0)?;
                let c_cell = region.assign_advice(
                    || "c",
                    self.config.col_c,
                    0,
                    || prev_b.value().copied() + prev_c.value(),
                )?;
                region.assign_fixed(
                    || "pa",
                    self.config.col_pa,
                    0,
                    || Value::
known(F::
from(125)),
                )?;
                Ok(c_cell)
            },
        )
    }
    pub fn expose_public(
        &self,
        mut layouter: impl Layouter<F>,
        cell: &AssignedCell<F, F>,
        row: usize,
    ) -> Result<(), Error> {
        layouter.constrain_instance(cell.cell(), self.config.instance, row)
    }
}
#[derive(Default, Serialize, Deserialize)]
pub struct FibonacciCircuit<F>(pub PhantomData<F>);
impl<F: FieldExt> Circuit<F> for FibonacciCircuit<F> {
    type Config = FibonacciConfig;
    type FloorPlanner = SimpleFloorPlanner;
    fn without_witnesses(&self) -> Self {
        Self::
default()
    }
    fn configure(meta: &mut ConstraintSystem<F>) -> Self::
Config {
        FibonacciChip::
configure(meta)
    }
    fn synthesize(
        &self,
        config: Self::
Config,
        mut layouter: impl Layouter<F>,
    ) -> Result<(), Error> {
        let chip = FibonacciChip::
construct(config);
        let (_, mut prev_b, mut prev_c) =
            chip.assign_first_row(layouter.namespace(|| "first row"))?;
        for _i in 3..5 {
            let c_cell = chip.assign_row(layouter.namespace(|| "next row"), &prev_b, &prev_c)?;
            prev_b = prev_c;
            prev_c = c_cell;
        }
        chip.expose_public(layouter.namespace(|| "out"), &prev_c, 2)?;
        Ok(())
    }
}
#[cfg(test)]
mod tests {
    use super::
FibonacciCircuit;
    use halo2_proofs::{dev::
MockProver, pasta::Fp};
    use std::
marker::
PhantomData;
    #[test]
    fn fibonacci_example1() {
        let k = 5;
        //1,2,3,5,?
        let a = Fp::
from(2); // F[0]
        let b = Fp::
from(3); // F[1]
        let out = Fp::
from(13); // F[6]
        let circuit = FibonacciCircuit(PhantomData);
        let mut public_input = vec![a, b, out];
        let prover = MockProver::
run(k, &circuit, vec![public_input.clone()]).unwrap();
        prover.assert_satisfied();
    }

}
use halo2_proofs::{
    arithmetic::
Field,
    circuit::{AssignedCell, Chip, Layouter, Region, Value},
    plonk::{Advice, Column, ConstraintSystem, Error, Expression, Instance, Selector, TableColumn},
    poly::
Rotation,
};
use std::
marker::
PhantomData;
const RANGE_BITS: usize = 8;
pub struct DivChip<F: Field> {
    pub config: DivConfig,
    _marker: PhantomData<F>,
}
// You could delete or add columns here
#[derive(Clone, Debug)]
pub struct DivConfig {
    // Dividend
    a: Column<Advice>,
    // Divisor
    b: Column<Advice>,
    // Quotient
    c: Column<Advice>,
    // Remainder
    r: Column<Advice>,
    // Aux
    k: Column<Advice>,
    // Range
    range: TableColumn,
    // Instance
    instance: Column,
    // Selector
    selector: Selector,
}
impl<F: Field> Chip<F> for DivChip<F> {
    type Config = DivConfig;
    type Loaded = ();
    fn config(&self) -> &Self::
Config {
        &self.config
    }
    fn loaded(&self) -> &Self::
Loaded {
        &()
    }
}
impl<F: Field> DivChip<F> {
    pub fn construct(config: <Self as Chip<F>>::
Config) -> Self {
        Self {
            config,
            _marker: PhantomData,
        }
    }
    pub fn configure(meta: &mut ConstraintSystem<F>) -> <Self as Chip<F>>::
Config {
        // Witness
        let col_a = meta.advice_column();
        let col_b = meta.advice_column();
        let col_c = meta.advice_column();
        let col_r = meta.advice_column();
        let col_k = meta.advice_column();
        // Selector
        let selector = meta.complex_selector();
        // Range
        let range = meta.lookup_table_column();
        // Instance
        let instance = meta.instance_column();
        meta.enable_equality(col_a);
        meta.enable_equality(col_b);
        meta.enable_equality(col_c);
        meta.enable_equality(col_r);
        meta.enable_equality(col_k);
        meta.enable_equality(instance);
        ///////////////////////// Please implement code here /////////////////////////
        meta.create_gate("mul", |meta| {
            let s = meta.query_selector(selector);
            let b = meta.query_advice(col_b, Rotation::
cur());
            let c = meta.query_advice(col_c, Rotation::
cur());
            let k = meta.query_advice(col_k, Rotation::
cur());
            println!("{:?}",s.clone() * (b.clone() * c.clone() - k.clone()));
            vec![s * (b * c - k)]
        });
        meta.create_gate("add", |meta| {
            let s = meta.query_selector(selector);
            let a = meta.query_advice(col_a, Rotation::
cur());
            let r = meta.query_advice(col_r, Rotation::
cur());
            let k = meta.query_advice(col_k, Rotation::
cur());
            println!("{:?}",s.clone() * (a.clone() - r.clone() - k.clone()));
            vec![s * (a - r - k)]
        });
        meta.create_gate("range check", |meta| {
            let s = meta.query_selector(selector);
            let mut constraints = vec![];
            let a = meta.query_advice(col_a, Rotation::
cur());
            let b = meta.query_advice(col_b, Rotation::
cur());
            let c = meta.query_advice(col_c, Rotation::
cur());
            let r = meta.query_advice(col_r, Rotation::
cur());
            let k = meta.query_advice(col_k, Rotation::
cur());
            let range_check = | a: Expression<F>| {
                let mut range = 255;
                let mut value = F::
ZERO;
                (1..range).fold(Expression::
Constant(F::
ONE), |expr, _| {
                    let result = expr * (Expression::
Constant(value) - a.clone());
                    value = value + F::
ONE;
                    result
                })
            };
            constraints.push(s.clone() * range_check(a.clone()));
            constraints.push(s.clone() * range_check(b.clone()));
            constraints.push(s.clone() * range_check(c.clone()));
            constraints.push(s.clone() * range_check(r.clone()));
            constraints.push(s.clone() * range_check(k.clone()));
            constraints
        });
        ///////////////////////// End implement /////////////////////////
        DivConfig {
            a: col_a,
            b: col_b,
            c: col_c,
            r: col_r,
            k: col_k,
            range,
            instance,
            selector,
        }
    }
    // Assign range for U8 range check
    pub fn assign_range(&self, mut layouter: impl Layouter<F>) -> Result<(), Error> {
        let config = &self.config;
        layouter.assign_table(
            || "range check table",
            |mut table| {
                let mut offset = 0;
                let mut value = F::
ZERO;
                for i in 0..(1 << RANGE_BITS )-1 {
                    table.assign_cell(|| "value", config.range, offset, || Value::
known(value))?;
                    offset += 1;
                    value = value + F::
ONE;
                }
                Ok(())
            },
        )?;
        Ok(())
    }
    // Assign witness for division
    pub fn assign_witness(
        &self,
        mut layouter: impl Layouter<F>,
        a: F,
        b: F,
        c: F,
    ) -> Result<AssignedCell<F, F>, Error> {
        let config = &self.config;
        let (c_cell, _) = layouter.assign_region(
            || "one row",
            |mut region| {
                config.selector.enable(&mut region, 0)?;
                let a_cell = region.assign_advice(
                    || "a",
                    config.a,
                    0,
                    || Value::
known(a),
                )?;
                let b_cell = region.assign_advice(
                    || "b",
                    config.b,
                    0,
                    || Value::
known(b),
                )?;
                let c_cell = region.assign_advice(
                    || "c",
                    config.c,
                    0,
                    || Value::
known(c),
                )?;
                let k_cell = region.assign_advice(
                    || "b * c",
                    config.k,
                    0,
                    || b_cell.value().copied() * c_cell.value(),
                )?;
                let r_cell = region.assign_advice(
                    || "r",
                    config.r,
                    0,
                    || a_cell.value().copied() - k_cell.value(),
                )?;
                Ok((c_cell, r_cell))
            },
        )?;
        Ok(c_cell)
    }
    pub fn expose_public(
        &self,
        mut layouter: impl Layouter<F>,
        cell: &AssignedCell<F, F>,
    ) -> Result<(), Error> {
        layouter.constrain_instance(cell.cell(), self.config.instance, 0)
    }
}
/* ================Circuit========================== */
use halo2_proofs::
circuit::
SimpleFloorPlanner;
use halo2_proofs::
plonk::
Circuit;
#[derive(Clone, Debug)]
pub struct CircuitConfig {
    config: DivConfig,
}
#[derive(Default, Debug)]
pub struct DivCircuit<F: Field> {
    pub a: F,
    pub b: F,
    pub c: F,
}
impl<F: Field> Circuit<F> for DivCircuit<F> {
    type Config = CircuitConfig;
    type FloorPlanner = SimpleFloorPlanner;
    #[cfg(feature = "circuit-params")]
    type Params = ();
    fn without_witnesses(&self) -> Self {
        Self::
default()
    }
    fn configure(meta: &mut ConstraintSystem<F>) -> Self::
Config {
        let config = DivChip::<F>::
configure(meta);
        CircuitConfig { config }
    }
    fn synthesize(
        &self,
        config: Self::
Config,
        mut layouter: impl Layouter<F>,
    ) -> Result<(), Error> {
        let chip = DivChip::<F>::
construct(config.config);
        chip.assign_range(layouter.namespace(|| "assign range"))?;
        let cell_c = chip.assign_witness(
            layouter.namespace(|| "assign witness"),
            self.a,
            self.b,
            self.c,
        )?;
        chip.expose_public(layouter.namespace(|| "expose public"), &cell_c)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use ff::
PrimeField;
    use halo2_proofs::
dev::
MockProver;
    use halo2curves::
bn256::Fr;
    #[test]
    fn sanity_check() {
        let k = 10;
        let a = Fr::
from_u128(10);
        let b = Fr::
from_u128(3);
        let c = Fr::
from_u128(3);
        let circuit: DivCircuit<Fr> = DivCircuit { a, b, c };
        let prover = MockProver::
run(k, &circuit, vec![vec![c]]).unwrap();
        assert_eq!(prover.verify(), Ok(()));
    }
}
use halo2_proofs::{
    plonk::{create_proof, keygen_pk, keygen_vk, verify_proof, ProvingKey},
    poly::
kzg::{
        commitment::{KZGCommitmentScheme, ParamsKZG},
        multiopen::{ProverGWC, VerifierGWC},
        strategy::
SingleStrategy,
    },
    transcript::{
        Blake2bRead, Blake2bWrite, Challenge255, TranscriptReadBuffer, TranscriptWriterBuffer,
    },
    SerdeFormat,
};
use halo2curves::
bn256::{Bn256, Fr, G1Affine};
use rand::
rngs::
OsRng;
use std::{
    fs::
File,
    io::{BufReader, BufWriter, Write},
};
fn generate_keys(k: u32, circuit: &DivCircuit<Fr>) -> (ParamsKZG, ProvingKey<G1Affine>) {
    let params = ParamsKZG::::
setup(k, OsRng);
    let vk = keygen_vk(&params, circuit).expect("vk should not fail");
    let pk = keygen_pk(&params, vk, circuit).expect("pk should not fail");
    (params, pk)
}
fn generate_proof(k: u32, circuit: DivCircuit<Fr>) {
    let (params, pk) = generate_keys(k, &circuit);
    let instances: &[&[Fr]] = &[&[circuit.c]];
    let f = File::
create(format!("{}", "proof")).unwrap();
    let mut proof_writer = BufWriter::
new(f);
    let mut transcript = Blake2bWrite::<_, _, Challenge255<_>>::
init(&mut proof_writer);
    create_proof::<
        KZGCommitmentScheme,
        ProverGWC<'_, Bn256>,
        Challenge255<G1Affine>,
        _,
        Blake2bWrite<_, G1Affine, Challenge255<_>>,
        _,
    >(
        &params,
        &pk,
        &[circuit],
        &[instances],
        OsRng,
        &mut transcript,
    )
        .expect("prover should not fail");
    let proof_writer = transcript.finalize();
    let _ = proof_writer.flush();
    // Dump params
    {
        let f = File::
create(format!("{}", "param")).unwrap();
        let mut writer = BufWriter::
new(f);
        params
            .write_custom(&mut writer, SerdeFormat::
RawBytes)
            .unwrap();
        let _ = writer.flush();
    }
    // Dump vk
    {
        let f = File::
create(format!("{}", "vk")).unwrap();
        let mut writer = BufWriter::
new(f);
        pk.get_vk()
            .write(&mut writer, SerdeFormat::
RawBytes)
            .unwrap();
        let _ = writer.flush();
    }
}
#[cfg(test)]
mod test {
    use super::*;
    use ff::
PrimeField;
    use halo2_proofs::
dev::
MockProver;
    use halo2curves::
bn256::Fr;
    #[test]
    fn sanity_check() {
        let k = 10;
        let a = Fr::
from_u128(10);
        let b = Fr::
from_u128(3);
        let c = Fr::
from_u128(3);
        let circuit: DivCircuit<Fr> = DivCircuit { a, b, c };
        let prover = MockProver::
run(k, &circuit, vec![vec![c]]).unwrap();
        assert_eq!(prover.verify(), Ok(()));

    }}‍
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/1-1708301194.jpeg)