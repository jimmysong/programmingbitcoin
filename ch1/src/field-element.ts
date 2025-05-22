export class FieldElement {
  private readonly num: number;
  private readonly prime: number;

  constructor(num: number, prime: number) {
    if (num >= prime || num < 0) {
      throw new Error(`Num ${num} not in field range 0 to ${prime - 1}`);
    }
    this.num = num;
    this.prime = prime;
  }

  toString(): string {
    return `FieldElement_${this.prime}(${this.num})`;
  }

  eq(other: FieldElement | null): boolean {
    return !!other && this.num === other.num && this.prime === other.prime;
  }

  ne(other: FieldElement | null): boolean {
    return !this.eq(other);
  }

  add(other: FieldElement): FieldElement {
    this.ensureSameField(other);
    const num = (this.num + other.num) % this.prime;  // % is used instead of calling the mod function because the result can't be -ve (% is more efficient than the mod function)
    return new FieldElement(num, this.prime);
  }

  sub(other: FieldElement): FieldElement {
    this.ensureSameField(other);
    const num = mod(this.num - other.num, this.prime);  // We call mod function because the result could be -ve
    return new FieldElement(num, this.prime);
  }

  mul(other: FieldElement): FieldElement {
    this.ensureSameField(other);
    const num = (this.num * other.num) % this.prime;
    return new FieldElement(num, this.prime);
  }

  pow(exponent: number): FieldElement {
    const n = mod(exponent, this.prime - 1);  // Fermat reduction
    const num = modPow(this.num, n, this.prime);  // Equivalent of pow() function in python
    return new FieldElement(num, this.prime);
  }

  div(other: FieldElement): FieldElement {
    this.ensureSameField(other);
    const inverse = modPow(other.num, this.prime - 2, this.prime);
    const num = (this.num * inverse) % this.prime;
    return new FieldElement(num, this.prime);
  }

  // Instead of doing this.prime !== other.prime in every operation, we use this helper function
  private ensureSameField(other: FieldElement): void {
    if (this.prime !== other.prime) {
      throw new TypeError('Cannot operate on numbers in different Fields');
    }
  }
}


// Call this mod function when the modding between 2 numbers could possibly return -ve results, like in sub, pow, and div
function mod(n: number, p: number): number {
  return ((n % p) + p) % p;
}

// This is the actual implementation of the built-in python function pow()
function modPow(base: number, exp: number, modn: number): number {
  let result = 1;
  base = mod(base, modn);
  let e = exp;
  while (e > 0) {
    if (e & 1) result = mod(result * base, modn);
    base = mod(base * base, modn);
    e >>= 1;
  }
  return result;
}
