import cv2
import numpy as np
import time

# =================================================================
# Course: Data Engineering (CSIE, Tamkang University)
# Lab 10: Spatial Manipulation & Interpolation Benchmarking
# =================================================================

def generate_4k_test_pattern():
    """
    Generates a 4K (3840x2160) high-frequency test image dynamically.
    The sharp lines and curves will clearly expose interpolation artifacts.
    """
    print("[*] Generating 4K test pattern in memory...")
    img = np.zeros((2160, 3840, 3), dtype=np.uint8)
    
    # Draw dense grid to test aliasing
    for i in range(0, 3840, 40):
        cv2.line(img, (i, 0), (i, 2160), (100, 100, 100), 2)
    for i in range(0, 2160, 40):
        cv2.line(img, (0, i), (3840, i), (100, 100, 100), 2)
        
    # Draw curves and text to test smoothness
    cv2.circle(img, (1920, 1080), 800, (0, 0, 255), 15)
    cv2.circle(img, (1920, 1080), 400, (0, 255, 255), 10)
    cv2.putText(img, "EDGE AI BENCHMARK", (350, 1100), 
                cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 255, 0), 25)
    return img

def benchmark_interpolation(img_4k, target_size=(224, 224), iterations=100):
    """
    Benchmarks three interpolation methods over N iterations.
    """
    print(f"[*] Starting benchmark: Scaling 4K to {target_size} over {iterations} iterations...")
    print("[!] Note: Running on GitHub VM. Absolute times are fast, focus on the RELATIVE GAP.\n")
    
    results = {}
    visuals = {}

    methods = [
        ("INTER_NEAREST", "TODO_FLAG_1"),
        ("INTER_LINEAR",  "TODO_FLAG_2"),
        ("INTER_CUBIC",   "TODO_FLAG_3")
    ]

    for name, flag in methods:
        times_ms = []
        resized_img = None
        
        # Warm-up run (to avoid CPU cold-start bias in VM)
        # cv2.resize(img_4k, target_size, interpolation=cv2.INTER_NEAREST)
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            
            # ---------------------------------------------------------
            # TODO 1, 2, 3: Perform the actual resize operation using OpenCV.
            # Replace the placeholder below with the correct cv2.resize call.
            # Pass the 'flag' variable to the interpolation parameter.
            # ---------------------------------------------------------
            if flag == "TODO_FLAG_1": interp_flag = cv2.INTER_NEAREST
            elif flag == "TODO_FLAG_2": interp_flag = cv2.INTER_LINEAR
            elif flag == "TODO_FLAG_3": interp_flag = cv2.INTER_CUBIC
            resized_img = cv2.resize(img_4k, target_size, interpolation=interp_flag)
            #pass # Remove this when implemented
            
            end_time = time.perf_counter()
            times_ms.append((end_time - start_time) * 1000)
            
        visuals[name] = resized_img
        
        # ---------------------------------------------------------
        # TODO 4: Calculate Statistical Metrics
        # Compute the mean and standard deviation of times_ms using NumPy.
        # ---------------------------------------------------------
        # mean_time = ...
        # std_time = ...
        
        mean_time = np.mean(times_ms) # Placeholder
        std_time = np.std(times_ms)  # Placeholder
        
        results[name] = (mean_time, std_time)

    return results, visuals

def render_comparison(visuals):
    """
    Stacks the images horizontally and adds labels for visual comparison.
    """
    print("[*] Rendering visual comparison to 'benchmark_visual_comparison.png'...")
    images = []
    
    for name, img in visuals.items():
        if img is None:
            print(f"[!] Warning: {name} image is missing. Did you complete TODO 1-3?")
            return
            
        # Add label background and text
        display_img = img.copy()
        cv2.rectangle(display_img, (0, 0), (224, 30), (0, 0, 0), -1)
        cv2.putText(display_img, name, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (255, 255, 255), 1)
        images.append(display_img)
        
    final_canvas = np.hstack(images)
    cv2.imwrite("benchmark_visual_comparison.png", final_canvas)
    print("[+] Done. Check your repository files for the image.\n")

if __name__ == "__main__":
    print("=== Week 10: VM Interpolation Benchmark ===\n")
    
    source_image = generate_4k_test_pattern()
    
    # Run the benchmark
    stats, images = benchmark_interpolation(source_image, target_size=(224, 224), iterations=100)
    
    # Calculate relative speed baseline (based on NEAREST if it exists)
    baseline_mean = stats.get("INTER_NEAREST", (0.0, 0.0))[0]
    
    # Print the Markdown Table
    print("| Method | Mean Latency (ms) | Std Dev (ms) | Relative Cost |")
    print("|---|---|---|---|")
    for name, (mean, std) in stats.items():
        if baseline_mean > 0:
            multiplier = mean / baseline_mean
            print(f"| {name} | {mean:.3f} | {std:.3f} | {multiplier:.1f}x |")
        else:
            print(f"| {name} | {mean:.3f} | {std:.3f} | N/A |")
    print("\n")
        
    # Render Output
    render_comparison(images)
