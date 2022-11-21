{
  description = "A flake for Meggie, MNE-python based M/EEG analysis software";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/9921c621ed25f7a2c64a7e3a95101e9ef7e8a4e6";

  outputs = { self, nixpkgs }:

    let pkgs = nixpkgs.legacyPackages.x86_64-linux;

    in {

      packages.x86_64-linux.meggie = import ./meggie.nix { pkgs=pkgs;};

      defaultPackage.x86_64-linux = self.packages.x86_64-linux.meggie;

    };
}
