def fibonacci_iterative(n):
    """
    Generate Fibonacci series up to n terms using iteration.
    
    Args:
        n (int): Number of terms to generate
        
    Returns:
        list: List containing the Fibonacci series
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def fibonacci_recursive(n):
    """
    Calculate the nth Fibonacci number using recursion.
    
    Args:
        n (int): Position in Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_generator():
    """
    Generate Fibonacci numbers using a generator.
    
    Yields:
        int: Next Fibonacci number in the sequence
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def main():
    print("Fibonacci Series Generator")
    print("-" * 30)
    
    # Get user input
    while True:
        try:
            n = int(input("Enter the number of terms to generate (or 0 to exit): "))
            if n == 0:
                break
            if n < 0:
                print("Please enter a positive number!")
                continue
                
            # Generate Fibonacci series using different methods
            print("\n1. Using Iteration:")
            fib_series = fibonacci_iterative(n)
            print(fib_series)
            
            print("\n2. Using Recursion:")
            fib_recursive = [fibonacci_recursive(i) for i in range(n)]
            print(fib_recursive)
            
            print("\n3. Using Generator (first", n, "terms):")
            fib_gen = fibonacci_generator()
            fib_generator_series = [next(fib_gen) for _ in range(n)]
            print(fib_generator_series)
            
        except ValueError:
            print("Please enter a valid number!")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        print("\n" + "-" * 30)

if __name__ == "__main__":
    main() 