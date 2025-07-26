package main

import (
    "fmt"
    "os"
    "strconv"
)

type Kernel struct {
    id   uint64
    data [64]uint64
}

func newKernel(id uint64) *Kernel {
    return &Kernel{id: id}
}

func (k *Kernel) performWork() {
    for i := range k.data {
            k.data[i] = k.id + uint64(i)
    }
}

func (k *Kernel) result() uint64 {
    return k.data[0]
}

func parseArg(name string, idx int) uint64 {
    if len(os.Args) <= idx {
        os.Exit(1)
    }
    v, err := strconv.ParseUint(os.Args[idx], 10, 64)
    if err != nil {
        os.Exit(1)
    }
    return v
}

func main() {
    iterations := parseArg("iterations", 1)
    arraySize := int(parseArg("array_size", 2))

    objects := make([]*Kernel, arraySize)
    var total uint64

    for i := uint64(0); i < iterations; i++ {
        idx := int(i % uint64(arraySize))

        objects[idx] = newKernel(i)
        k := objects[idx]

        k.performWork()
        total += k.result()
    }

    fmt.Printf("Go version completed, total = %d\n", total)
}