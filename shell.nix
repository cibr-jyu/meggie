{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "meggie-env";
  targetPkgs = pkgs: (with pkgs; [
    python39Full
    python39Packages.pip
    python39Packages.pyqt5
    python39Packages.wheel
    python39Packages.twine
    python39Packages.importlib-metadata
    python39Packages.zipp
    python39Packages.colorama
    python39Packages.requests
    python39Packages.urllib3
    python39Packages.chardet
    python39Packages.certifi
    python39Packages.idna
    python39Packages.setuptools
    python39Packages.pkginfo
    python39Packages.requests-toolbelt
    python39Packages.tqdm
    python39Packages.keyring
    python39Packages.rfc3986
    qt5Full
    glib
    zlib
    xorg.libX11
    xorg.libXrender
  ]);
  runScript = "bash prepare-nix.sh";
}).env
