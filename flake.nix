{ pkgs }:

let
  pythonEnv = pkgs.python3.withPackages (ps: [
    ps.tkinter
  ]);
in
pkgs.stdenv.mkDerivation {
  pname = "winspy";
  version = "1.0";

  src = ./.;

  # NativeBuildInputs for tools used during the build
  nativeBuildInputs = [ pkgs.makeWrapper ];
  buildInputs = [ pythonEnv ];

  installPhase = ''
    mkdir -p $out/bin
    cp winspy.py $out/bin/winspy.py

    # Create a wrapper that calls python with your script
    makeWrapper ${pythonEnv}/bin/python $out/bin/winspy \
      --add-flags "$out/bin/winspy.py" \
      --prefix PATH : ${
        pkgs.lib.makeBinPath [
          pkgs.hyprland
          pkgs.jq
        ]
      }
  '';
}
