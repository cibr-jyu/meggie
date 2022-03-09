{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "meggie-env";
  targetPkgs = pkgs: (with pkgs; [
    python39
    python39Packages.pip
    python39Packages.pyqt5
    qt5Full
    glib
    zlib
    xorg.libX11
    xorg.libXrender
  ]);
  runScript = "bash prepare-nix.sh";
}).env
