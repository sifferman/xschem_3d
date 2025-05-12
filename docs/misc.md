
# Miscellaneous Notes

## FFMPEG GIF

```bash
ffmpeg -i input.mkv -vf "fps=10,scale=720:-1:flags=lanczos" -c:v gif output.gif
```

## Digital Source

For the [Digital Source](https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Digital_Source) model, there is poor documentation for the `".stim"` file format. Here is a guide created by looking at the source code.

| **Token** | **Bit Value** | **State**   | **Strength**      |
|-----------|---------------|-------------|-------------------|
| `0s`      | 0             | ZERO        | STRONG            |
| `1s`      | 1             | ONE         | STRONG            |
| `Us`      | 2             | UNKNOWN     | STRONG            |
| `0r`      | 3             | ZERO        | RESISTIVE         |
| `1r`      | 4             | ONE         | RESISTIVE         |
| `Ur`      | 5             | UNKNOWN     | RESISTIVE         |
| `0z`      | 6             | ZERO        | HI_IMPEDANCE      |
| `1z`      | 7             | ONE         | HI_IMPEDANCE      |
| `Uz`      | 8             | UNKNOWN     | HI_IMPEDANCE      |
| `0u`      | 9             | ZERO        | UNDETERMINED      |
| `1u`      | 10            | ONE         | UNDETERMINED      |
| `Uu`      | 11            | UNKNOWN     | UNDETERMINED      |

* **Tokens**: These are the strings you use in the digital source input file (`dfxtp.stim`).
* **Bit Value**: Internal representation of the token in `ngspice`.
* **State**: Logical state (`ZERO`, `ONE`, `UNKNOWN`) represented by the token.
* **Strength**:
    * **STRONG**: Direct and confident assertion of the state.
    * **RESISTIVE**: Weakly pulled to the state.
    * **HI_IMPEDANCE**: High-impedance, allowing external influence.
    * **UNDETERMINED**: Undefined behavior or weak signal.

### Sources

* <https://sourceforge.net/p/ngspice/ngspice/ci/a42ea984719984a86c2cd915ca0310470ef3f892/tree/src/xspice/icm/digital/d_source/cfunc.mod#l536>
* <https://sourceforge.net/p/ngspice/ngspice/ci/a42ea984719984a86c2cd915ca0310470ef3f892/tree/src/xspice/icm/digital/d_source/cfunc.mod#l801>
