{ pkgs }:

let

  packageOverrides =
    self: super:
      # Read dependencies resolved with pip2nix
      let overrides =
        (import ./python-packages.nix {
           inherit pkgs;
           inherit (pkgs) fetchurl fetchgit fetchhg;
         }) self super;
      in
      {
        # Use only dependencies not available in nixpkgs
        inherit (overrides)
        "darkdetect"
        "h5io"
        "mne"
        "mne-qt-browser"
        "pyqtgraph"
        "scooby";
      };

  python = (pkgs.python39.override {
    inherit packageOverrides;
  });

in

python.pkgs.buildPythonApplication rec {
  pname = "meggie";
  version = "1.4.1";

  src = ./.;

  propagatedBuildInputs = with python.pkgs;
    [
      setuptools
      matplotlib
      pyqt5
      h5io
      scikit-learn
      python-json-logger
      mne
      mne-qt-browser
    ];

  nativeBuildInputs = with pkgs; [
    qt5.wrapQtAppsHook
  ];

  postFixup = ''
    wrapProgram $out/bin/meggie \
      "''${qtWrapperArgs[@]}"
  '';

  meta = with pkgs.lib; {
    homepage = "https://github.com/cibr-jyu/meggie";
    description = "User-friendly MNE-python based graphical user interface to do MEG and EEG analysis with multiple subjects";
    license = licenses.bsd3;
  };
}
