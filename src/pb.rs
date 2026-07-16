//! Generated protobuf / tonic clients (crate-private).
//!
//! Module nesting matches prost's `super::model::v1::…` paths.

#![allow(clippy::all)]
#![allow(dead_code)]
#![allow(missing_docs)]

pub mod genjutsu {
    pub mod myconversation {
        pub mod model {
            pub mod v1 {
                include!(concat!(
                    env!("OUT_DIR"),
                    "/genjutsu.myconversation.model.v1.rs"
                ));
            }
        }

        pub mod v1 {
            include!(concat!(env!("OUT_DIR"), "/genjutsu.myconversation.v1.rs"));
        }
    }
}
