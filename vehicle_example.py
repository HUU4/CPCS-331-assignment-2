from semantic_net import SemanticNet


def build_vehicle_example() -> SemanticNet:
    """
    Build the small, clean vehicle semantic net:
        Vehicle
        ├─ Car
        │   └─ Electric Car
        └─ Truck

    With parts: Engine, Wheel, Battery
    And fuels: Petrol, Diesel, Electricity
    """
    net = SemanticNet()

    # --- is-a relations ---
    net.add_is_a("Car", "Vehicle")
    net.add_is_a("Truck", "Vehicle")
    net.add_is_a("Electric Car", "Car")

    # --- parts ---
    net.add_has_part("Vehicle", "Engine")
    net.add_has_part("Vehicle", "Wheel")
    net.add_has_part("Electric Car", "Battery")

    # --- fuel usage ---
    net.add_uses_fuel("Car", "Petrol")
    net.add_uses_fuel("Truck", "Diesel")
    net.add_uses_fuel("Electric Car", "Electricity")

    return net


if __name__ == "__main__":
    # Build example net
    net = build_vehicle_example()

    # ---- BEFORE INFERENCE ----
    print("\nBefore inheritance:")
    print("Parts of Car:", net.neighbors_with_relation("Car", "has-part"))

    # Draw BEFORE inference
    net.draw("Semantic Net BEFORE Inference")

    # ---- PERFORM INFERENCE ----
    new_facts = net.inherit_properties(["has-part"])
    print("\nNewly inferred facts:", new_facts)

    print("After inheritance:")
    print("Parts of Car:", net.neighbors_with_relation("Car", "has-part"))

    # ---- Draw AFTER inference ----
    net.draw("Semantic Net AFTER Inference")

    # ---- CONFLICT EXAMPLE ----
    # Create a conflict intentionally: Car uses two fuels
    net.add_uses_fuel("Car", "Electricity")
    print("\nConflicts for relation 'uses-fuel':", net.find_conflicts("uses-fuel"))
