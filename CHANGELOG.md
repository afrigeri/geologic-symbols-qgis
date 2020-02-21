# Change Log

All notable changes to the gsymblib project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased][]

### Changed

### Added

- SVG to TinySVG conversion during the build process. Done with svg2svgt (LGPL Nokia).

## [1.0.0-rc.1] - 2019-10-16

### Changed

- QGIS minimum version is 3.8.x-Zanzibar, support of Hashed Line symbol type

### Added

- issue tracker tag __new symbol__ for new symbols
- issue tracker tag __symbol fix__ for fixes to existing symbols 
- Added 7 strike slip fault symbols [@valemercurii](https://github.com/valemercurii)
- Added 4 thrust fault symbols [@valemercurii](https://github.com/valemercurii)
- Added 44 new symbols [@marchunterUSGS](https://github.com/marchunterUSGS)
- Added graphical representation of the symbols in the STATUS page
- Added 31 new symbols [@erikaluzzi](https://github.com/erikaluzzi)
- Fixed code for the generation of symboll list [@luca-penasa](https://github.com/luca-penasa)
- Added basic validation to the library generator [@luca-penasa](https://github.com/luca-penasa)

### Removed

- wrong fgdc SVG pattern directory (typo) [@chbrandt](https://github.com/chbrandt)

### Known Issues

- Qt5 of QGIS supports SVG Tiny 1.2. Pattern of symbols fgdc 25.128 25.129 25.133 use 
ClipPath which is defined in SVG 2.  The fills are rendered as all black.  We need to 
convert these patterns into SVG Tiny 1.2 compatible ones.
