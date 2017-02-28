
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import semantics


def generate(data, filename="default.svg"):
    """
        data format should be a list of (ingredient, weight in kg) tuples
        e.g: [("beef", 0.2), ("tomato", 0.14), ("peanut", 0.05)]
    """
    impact, quantities = semantics.process_ingredients_impact(data)
    print(impact, quantities)
    plt.xkcd()


    fig = plt.figure(figsize=(10, 6))
    ax1 = plt.subplot(1, 2, 1)

    # The slices will be ordered and plotted counter-clockwise.
    labels = list(impact.keys())
    sizes1 = list(impact.values())

    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange']

    plt.pie(sizes1, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title("Share of the \nenvironmental impact", y=0.95)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    ax2 = plt.subplot(1, 2, 2)
    sizes2 = list(quantities.values())
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange']
    # The slices will be ordered and plotted counter-clockwise.

    plt.pie(sizes2, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title("Share of the \nenvironmental impact", y=0.95)

    plt.axis('equal')
    plt.tight_layout(4, 0, 5)
    plt.savefig(filename)

    return

generate([("beef", 200), ("fresh tomato", 300), ("peanut", 50), ("carrot", 40), ("sugar", 100)], "test.png")
