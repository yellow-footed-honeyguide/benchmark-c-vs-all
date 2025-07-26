use std::env;

#[derive(Clone)]
struct Kernel {
    id: u64,
    data: [u64; 64],
}

impl Kernel {
    fn new(id: u64) -> Self {
        Kernel { id, data: [0; 64] }
    }

    fn perform_work(&mut self) {
        for (i, slot) in self.data.iter_mut().enumerate() {
            *slot = self.id + i as u64;
        }
    }

    fn result(&self) -> u64 {
        self.data[0]
    }
}

fn parse_arg<T: std::str::FromStr>(arg: Option<String>) -> T {
    arg.and_then(|s| s.parse::<T>().ok()).unwrap()
}

fn main() {
    let mut args = env::args();
    let _ = args.next(); // skip program name

    let iterations: u64 = parse_arg(args.next());
    let array_size: usize = parse_arg(args.next());

    let mut objects: Vec<Option<Box<Kernel>>> = vec![None; array_size];
    let mut total: u64 = 0;

    for i in 0..iterations {
        let idx = (i as usize) % array_size;

        // free old, allocate new
        objects[idx] = Some(Box::new(Kernel::new(i)));
        let kernel = objects[idx].as_mut().unwrap();

        kernel.perform_work();
        total = total.wrapping_add(kernel.result());
    }

    println!("Rust version completed, total = {}", total);
}
