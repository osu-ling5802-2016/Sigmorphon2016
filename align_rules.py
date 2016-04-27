# -*- coding: utf-8 -*-i
import operator
import sys

infile_name = sys.argv[1]

rules = [ ]

with open(infile_name, encoding = "utf-8") as infile:
  for line in infile:
    # Get the length of the original word. This can be used to indicate
    # relative changes.
    comps = line.rstrip().split("\t")
    word_length = len(comps[0])

    # Get the attributes.
    attr_dict = { }

    attrs = comps[1]
    attrs_comps = attrs.split(",")
    for attr in attrs_comps:
      attr_comps = attr.split("=")
      name = attr_comps[0]
      val = attr_comps[1]

      attr_dict[name] = val

    # Get the list of changes.
    change_list = [ ]

    new_word = comps[2]

    print(comps)

    changes = comps[4]
    if changes != "None":
      change_comps = changes.split(";")
      index = 0
      for change in change_comps:
        index += 1
        parts = change.replace("(", "").replace(")", "").split(",")
        first_char = parts[0]
        second_char = parts[1]

        if first_char != second_char: 
          change_list.append(str(index) + "-" + first_char + "/" + second_char)

    rules.append((attr_dict, change_list, comps[0], new_word))

attr_dict = { }

for i in range(len(rules)):
  for j in range(i, len(rules)):
    # Compare two rules to one another.
    attr_1, list_1, base_1, infl_1 = rules[i]
    attr_2, list_2, base_2, infl_2 = rules[j]

    if abs(len(attr_1) - len(attr_2)) < 2:
      # One attribute was added, or one was modified.
      if len(attr_1) == len(attr_2):
        # Check if only one attribute was modified.
        has_same_attr = True

        for attr_name in attr_1:
          if not attr_name in attr_2:
            has_same_attr = False

        if has_same_attr:
          # They have the same attributes, so check to see how many of the
          # values are different.
          num_differences = 0
          last_different_attr_name = ""
          last_different_attr_val = ""

          for attr_name in attr_1:
            val_1 = attr_1[attr_name]
            val_2 = attr_2[attr_name]
            if val_1 != val_2:
              last_different_attr_name = attr_name
              last_different_attr_val = val_1 + "~" + val_2
              num_differences += 1

          # ONLY care if the number of differences is 1.
          if num_differences == 1:
            # Get the attribute string value.
            attr_str_val = ""

            for attr_name, val in attr_1.items():
              if attr_name != last_different_attr_name:
                attr_str_val += attr_name + "=" + val + ","

            attr_diff = last_different_attr_name + "\t" + last_different_attr_val + "\t" + attr_str_val
            if not attr_diff in attr_dict:
              attr_dict[attr_diff] = [ ]
            attr_dict[attr_diff].append((list_1, list_2))

            print(attr_diff)
            print(list_1)
            print(list_2)
      elif abs(len(attr_1) - len(attr_2)) == 1:
        same_base = True

        extra_attr = ""
        extra_val = ""
        base_val = ""

        smaller = list_1
        bigger = list_2

        # Check which has more.
        if len(attr_1) > len(attr_2):
          for attr_name in attr_2:
            if not attr_name in attr_1:
              same_base = False
              break
            elif attr_1[attr_name] != attr_2[attr_name]:
              same_base = False
              break
            else:
              base_val += attr_name + "=" + attr_2[attr_name] + ","
          if same_base:
            for attr_name in attr_1:
              if not attr_name in attr_2:
                extra_attr = attr_name
                extra_val = attr_1[attr_name]
                break
          bigger, smaller = smaller, bigger
        else:
          for attr_name in attr_1:
            if not attr_name in attr_2:
              same_base = False
              break
            elif attr_1[attr_name] != attr_2[attr_name]:
              same_base = False
              break
            else:
              base_val += attr_name + "=" + attr_1[attr_name] + ","
          if same_base:
            for attr_name in attr_2:
              if not attr_name in attr_1:
                extra_attr = attr_name
                extra_val = attr_2[attr_name]
                break

        if same_base:
          attr_diff = extra_attr + "\t~" + extra_val + "\t" + base_val
          if not attr_diff in attr_dict:
            attr_dict[attr_diff] = [ ]
          attr_dict[attr_diff].append((smaller, bigger))

          print(attr_diff)
          print(smaller)
          print(bigger)

for attr_type, change_list in attr_dict.items():
  print("***** NEW ATTRIBUTE *****")
  attr_comps = attr_type.split("\t")
  attr_name = attr_comps[0]
  attr_vals = attr_comps[1]
  base_vals = attr_comps[2]

  val_changes = att_vals.split("~")
  orig_val = val_changes[0]
  new_val = val_changes[1]

  if orig_val == "":
    orig_val = "none"

  print("With base form " + base_vals + ", changing " + attr_name + " from " + orig_val + " to " + new_val)
  
  # for manip_1, manip_2 in change_list:
