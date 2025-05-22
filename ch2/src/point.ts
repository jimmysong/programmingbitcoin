export class Point {
  public readonly x: number | null;
  public readonly y: number | null;

  public readonly a: number;
  public readonly b: number;

  constructor(x: number | null, y: number | null, a: number, b: number) {
    this.x = x;
    this.y = y;
    this.a = a;
    this.b = b;

    if (x === null && y === null) return;

    if (y! ** 2 !== x! ** 3 + a * x! + b) {
      throw new Error(`(${x}, ${y}) is not on the curve`);
    }
  }

  toString(): string {
    return this.x === null
      ? 'Point(infinity)'
      : `Point(${this.x},${this.y})_${this.a}_${this.b}`;
  }

  eq(other: Point | null): boolean {
    return (
      !!other &&
      this.x === other.x &&
      this.y === other.y &&
      this.a === other.a &&
      this.b === other.b
    );
  }

  ne(other: Point | null): boolean {
    return !this.eq(other);
  }

  add(other: Point): Point {
    if (this.a !== other.a || this.b !== other.b) {
      throw new TypeError(`Points ${this} and ${other} are not on the same curve`);
    }

    if (this.x === null) return other;
    if (other.x === null) return this;

    // Case 1: P.x == Q.x but P.y ≠ Q.y  →  ∞
    if (this.x === other.x && this.y !== other.y) {
      return new Point(null, null, this.a, this.b);
    }

    let s: number;

    // Case 2: distinct x-coordinates
    if (this.x !== other.x) {
      s = (other.y! - this.y!) / (other.x - this.x);
    }

    // Case 3 & 4: doubling (P == Q)
    else {
      if (this.y === 0) {  // Tangent is vertical ⇒ result is ∞
        return new Point(null, null, this.a, this.b);
      }
      s = (3 * this.x ** 2 + this.a) / (2 * this.y!);
    }

    const x3 = s ** 2 - this.x - other.x;
    const y3 = s * (this.x - x3) - this.y!;
    return new Point(x3, y3, this.a, this.b);
  }
}
