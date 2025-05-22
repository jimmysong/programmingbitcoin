import { FieldElement } from './field-element';

describe('FieldElement', () => {
  test('ne', () => {
    const a = new FieldElement(2, 31);
    const b = new FieldElement(2, 31);
    const c = new FieldElement(15, 31);
    expect(a.eq(b)).toBe(true);
    expect(a.ne(c)).toBe(true);
    expect(a.ne(b)).toBe(false);
  });

  test('add', () => {
    let a = new FieldElement(2, 31);
    let b = new FieldElement(15, 31);
    expect(a.add(b).eq(new FieldElement(17, 31))).toBe(true);

    a = new FieldElement(17, 31);
    b = new FieldElement(21, 31);
    expect(a.add(b).eq(new FieldElement(7, 31))).toBe(true);
  });

  test('sub', () => {
    let a = new FieldElement(29, 31);
    let b = new FieldElement(4, 31);
    expect(a.sub(b).eq(new FieldElement(25, 31))).toBe(true);

    a = new FieldElement(15, 31);
    b = new FieldElement(30, 31);
    expect(a.sub(b).eq(new FieldElement(16, 31))).toBe(true);
  });

  test('mul', () => {
    const a = new FieldElement(24, 31);
    const b = new FieldElement(19, 31);
    expect(a.mul(b).eq(new FieldElement(22, 31))).toBe(true);
  });

  test('pow', () => {
    let a = new FieldElement(17, 31);
    expect(a.pow(3).eq(new FieldElement(15, 31))).toBe(true);

    a = new FieldElement(5, 31);
    const b = new FieldElement(18, 31);
    expect(a.pow(5).mul(b).eq(new FieldElement(16, 31))).toBe(true);
  });

  test('div', () => {
    let a = new FieldElement(3, 31);
    let b = new FieldElement(24, 31);
    expect(a.div(b).eq(new FieldElement(4, 31))).toBe(true);

    a = new FieldElement(17, 31);
    expect(a.pow(-3).eq(new FieldElement(29, 31))).toBe(true);

    a = new FieldElement(4, 31);
    b = new FieldElement(11, 31);
    expect(a.pow(-4).mul(b).eq(new FieldElement(13, 31))).toBe(true);
  });
});
