import { Point } from './point';

describe('Point', () => {
  test('ne', () => {
    const a = new Point(3, -7, 5, 7);
    const b = new Point(18, 77, 5, 7);
    expect(a.ne(b)).toBe(true);
    expect(a.ne(a)).toBe(false);
  });

  test('add – identity & inverses', () => {
    const inf = new Point(null, null, 5, 7);
    const p  = new Point(2, 5, 5, 7);
    const n  = new Point(2, -5, 5, 7);     // −p
    expect(inf.add(p).eq(p)).toBe(true);
    expect(p.add(inf).eq(p)).toBe(true);
    expect(p.add(n).eq(inf)).toBe(true);
  });

  test('add – distinct points', () => {
    const a = new Point(3, 7, 5, 7);
    const b = new Point(-1, -1, 5, 7);
    expect(a.add(b).eq(new Point(2, -5, 5, 7))).toBe(true);
  });

  test('add – doubling', () => {
    const a = new Point(-1, -1, 5, 7);
    expect(a.add(a).eq(new Point(18, 77, 5, 7))).toBe(true);
  });
});
