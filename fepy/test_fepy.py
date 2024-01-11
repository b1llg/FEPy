import fepy

def main():
    u = fepy.Field("u",np.array(["u"]))

    model = fepy.Model("input.txt", np.array([u]))

    print(model.tdofs)
    # fem_data.SetTotalDofs()

    # print(fem_data.tdof)

if __name__ == "__main__":
    main()
