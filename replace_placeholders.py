import json
import os

# Define the clusters for Phase 18 (Final Collection)
CLUSTERS = [
    {
        "id": "castor_wheel",
        "keywords": ["CASTER", "WHEEL", "CASTOR"],
        "target_name": "hardware-castor-wheel-v1.png",
        "prompt": "Heavy-duty industrial swivel castor wheel with steel frame and rubber wheel, high-quality hardware store product photography, isolated on white background.",
        "category": "TOOLS"
    },
    {
        "id": "nylon_rope",
        "keywords": ["ROPE", "NYLON", "MANILA"],
        "target_name": "nylon-rope-roll-v1.png",
        "prompt": "Large coiled roll of braided white and blue nylon rope, professional hardware packaging, high-quality product photography, isolated on white background.",
        "category": "MISC"
    },
    {
        "id": "manhole_cover",
        "keywords": ["MAN HOLE", "MANHOLE", "COVER"],
        "target_name": "manhole-cover-metal-v1.png",
        "prompt": "Heavy cast iron manhole cover, round with textured anti-slip surface, industrial hardware product photography, sharp metallic detail, isolated on white background.",
        "category": "BUILDING MATERIALS"
    },
    {
        "id": "drawer_slides",
        "keywords": ["DRAWER RAIL", "DRAWER SLIDE", "DRAWER RAILS"],
        "target_name": "drawer-slide-ball-bearing-v1.png",
        "prompt": "Pair of telescopic ball-bearing drawer slides, galvanized steel, silver metallic finish, high-quality hardware product photography, isolated on white background.",
        "category": "IRONMONGERY"
    },
    {
        "id": "welding_electrodes",
        "keywords": ["WELDING", "ELECTRODE"],
        "target_name": "welding-electrode-pack-v1.png",
        "prompt": "Industrial pack of welding electrodes, steel rods visible, professional cardboard packaging, hardware store product photography, isolated on white background.",
        "category": "TOOLS"
    },
    {
        "id": "curtain_rod",
        "keywords": ["CURTAIN ROD", "CURTAIN DECO"],
        "target_name": "curtain-rod-finial-v1.png",
        "prompt": "Premium brushed nickel curtain r with decorative ball finials, modern hardware design, high-quality product photography, isolated on white background.",
        "category": "DECORATIVE"
    },
    {
        "id": "tank_connector",
        "keywords": ["TANK CONNECTOR"],
        "target_name": "pvc-tank-connector-v1.png",
        "prompt": "Heavy-duty black PVC tank connector fitting, threaded with rubber gasket, industrial plumbing photography, isolated on white background.",
        "category": "PLUMBING"
    },
    {
        "id": "gate_decoration",
        "keywords": ["GATE DECORATION"],
        "target_name": "gate-decoration-steel-v1.png",
        "prompt": "Decorative wrought iron steel element for gate designs, ornamental scrollwork, metallic finish, isolated on white background.",
        "category": "BUILDING MATERIALS"
    },
    {
        "id": "masonry_bit",
        "keywords": ["MANSON BIT", "MASONRY BIT", "MANSON BITS"],
        "target_name": "masonry-drill-bit-v1.png",
        "prompt": "High-quality carbide-tip masonry drill bit, silver steel finish, industrial tool photography, isolated on white background.",
        "category": "TOOLS"
    },
    {
        "id": "edge_banding",
        "keywords": ["LIPPING", "RIPPING", "EDGE BANDING"],
        "target_name": "edge-banding-veneer-v1.png",
        "prompt": "Roll of wood veneer edge banding, professional carpentry material, high-quality product photography, isolated on white background.",
        "category": "BOARDS"
    },
    {
        "id": "circuit_breaker",
        "keywords": ["CIRCUIT BREAKER", "CIRCUIT BR", "MCB "],
        "target_name": "circuit-breaker-mcb-v1.png",
        "prompt": "Modern white miniature circuit breaker (MCB), electrical component, professional photography, isolated on white background.",
        "category": "ELECTRICALS"
    },
    {
        "id": "consumer_unit",
        "keywords": ["CONSUMER UNIT", "CONSUME UNIT", "DISTRIBUTION BOARD"],
        "target_name": "electrical-consumer-unit-v1.png",
        "prompt": "White plastic electrical consumer unit casing, distribution board for home wiring, professional photography, isolated on white background.",
        "category": "ELECTRICALS"
    },
    {
        "id": "multi_plug",
        "keywords": ["MULTIPLUG", "MULTI PLUG", "MULTI-PLUG"],
        "target_name": "multi-plug-adapter-v1.png",
        "prompt": "White 3-way electrical multi-plug adapter, high-quality plastic finish, professional photography, isolated on white background.",
        "category": "ELECTRICALS"
    },
    {
        "id": "gutters",
        "keywords": ["GUTTER", "DOWN PIPE", "PTG "],
        "target_name": "pvc-rainwater-gutter-v1.png",
        "prompt": "White PVC rainwater gutter section with end cap, modern residential drainage system, high-quality product photography, isolated on white background.",
        "category": "BUILDING MATERIALS"
    },
    {
        "id": "saddle_clamps",
        "keywords": ["SADDLE CLAMP"],
        "target_name": "saddle-clamp-steel-v1.png",
        "prompt": "High-quality galvanized steel saddle clamp for heavy pipe support, industrial hardware photography, isolated on white background.",
        "category": "PLUMBING"
    },
    {
        "id": "adhesives",
        "keywords": ["HENKEL", "TANGIT", "WOOD GLU", "MARINE FEVICOL"],
        "target_name": "industrial-glue-can-v1.png",
        "prompt": "Large professional metal can of industrial wood glue, brand label visible, carpentry workshop setting or plain background, isolated on white background.",
        "category": "ADHESIVES"
    },
    {
        "id": "polythene_paper",
        "keywords": ["POLYTHENE BLACK", "DAMP PROOF"],
        "target_name": "polythene-sheet-roll-v1.png",
        "prompt": "Large roll of heavy-duty black polythene plastic sheeting, damp proof membrane, construction material photography, isolated on white background.",
        "category": "BUILDING MATERIALS"
    },
    {
        "id": "gate_roller",
        "keywords": ["GATE ROLLER", "GATE ROLLLL"],
        "target_name": "sliding-gate-roller-v1.png",
        "prompt": "Steel sliding gate roller with ball bearing, heavy-duty metallic hardware, gate mechanism photography, isolated on white background.",
        "category": "IRONMONGERY"
    },
    {
        "id": "metal_tube",
        "keywords": ["TUBE", "SQ8", "SQ12", "SQ16", "G14", "G16", "G18"],
        "target_name": "hardware-metal-tube-v1.png",
        "prompt": "Sleek bundle of hollow steel tubes, square and round sections, galvanized metallic finish, industrial hardware product photography, isolated on white background.",
        "category": "METAL SECTIONS"
    }
]

def update_placeholders():
    json_path = 'src/assets/data/products.json'
    with open(json_path, 'r') as f:
        products = json.load(f)

    updated_count = 0
    mapped_clusters = set()
    
    for p in products:
        name = p.get('name', '').upper()
        current_img = p.get('image', '')
        
        # Only replace if using a generic placeholder
        if any(x in current_img for x in ['tools.jpg', 'paints.jpg', 'electricals.jpg']):
            for cluster in CLUSTERS:
                if any(k in name for k in cluster['keywords']):
                    p['image'] = f"assets/images/products/hardware/{cluster['target_name']}"
                    p['images'] = [p['image']]
                    updated_count += 1
                    mapped_clusters.add(cluster['id'])
                    break

    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Mapped {updated_count} products across {len(mapped_clusters)} clusters.")

if __name__ == "__main__":
    update_placeholders()
