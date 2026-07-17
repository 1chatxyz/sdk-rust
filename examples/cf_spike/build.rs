fn main() -> Result<(), Box<dyn std::error::Error>> {
    let proto_root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../proto");
    let proto_root = proto_root.canonicalize()?;
    println!("cargo:rerun-if-changed={}", proto_root.display());
    let main_proto = proto_root.join("myconversation/api/myconversation.proto");
    tonic_prost_build::configure()
        .build_server(false)
        .build_client(true)
        .build_transport(false)
        .compile_protos(&[main_proto], &[proto_root])?;
    Ok(())
}
