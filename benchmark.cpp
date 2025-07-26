#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <stdio.h>
#include <vector>

using std::size_t;
using std::uint64_t;

class Kernel {
public:
  explicit Kernel(uint64_t id) noexcept : id(id) { data.fill(0); }
  void perform_work() noexcept {
    for (size_t i = 0; i < data.size(); ++i) {
      data[i] = id + i;
    }
  }

  uint64_t get_data(size_t index) const noexcept { return data[index]; }

private:
  uint64_t id;
  std::array<uint64_t, 64> data;
};

int main(int argc, char *argv[]) {
  const uint64_t iterations = std::strtoull(argv[1], nullptr, 10);
  const size_t array_size = std::strtoull(argv[2], nullptr, 10);

  std::vector<std::unique_ptr<Kernel>> objects;
  objects.resize(array_size);

  uint64_t total = 0;

  for (uint64_t i = 0; i < iterations; i++) {
    size_t idx = static_cast<size_t>(i % array_size);

    // allocate new object, destructing old one
    objects[idx] = std::make_unique<Kernel>(i);
    objects[idx]->perform_work();

    total += objects[idx]->get_data(0);
  }

  std::cout << "C++ version completed, total = " << total << '\n';
  return EXIT_SUCCESS;
}
