# -*- coding: utf-8 -*-i
import operator
import sys

infile_name = sys.argv[1]

rules = [ ]

def find_dif(list_1, list_2):
  shorter_len = len(list_1)
  if len(list_2) < shorter_len:
    shorter_len = len(list_2)

  same_index_front = 0
  for i in range(shorter_len):
    if list_1[i] == list_2[i]:
      same_index_front += 1
    else:
      break

  same_index_back = 0
  for i in range(1, shorter_len + 1):
    if list_1[len(list_1) - i] == list_2[len(list_2) - i]:
      same_index_back += 1
    else:
      break

  list_1_val = ""
  for val in list_1:
    list_1_val += val.split(",")[2]
  list_2_val = ""
  for val in list_2:
    list_2_val += val.split(",")[2]

  if same_index_front > 0 or same_index_back > 0:
    first_suffix = ""
    for j in range(same_index_front, len(list_1) - same_index_back):
      first_suffix += list_1[j].split(",")[2]
    second_suffix = ""
    for j in range(same_index_front, len(list_2) - same_index_back):
      second_suffix += list_2[j].split(",")[2]

    return first_suffix + "~" + second_suffix
  else:
    return ""


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

    changes = comps[3]
    if changes != "None":
      change_comps = changes.split("|")
      index = 0
      for change in change_comps:
        change_text = change.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        parts = change_text.split(",")
        function = parts[0]
        orig_index = int(parts[1])
        final_index = int(parts[2])

        change_str = ""

        if orig_index == 0:
          # Prefix.
          change_str = "p"
        elif final_index >= orig_index:
          # Suffix.
          orig_index = word_length - orig_index
          change_str = "s" + str(orig_index)
        else:
          # Infix.
          change_str = "i" + str(orig_index)

        change_list.append(function + "," + change_str + "," + new_word[final_index])

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
            val_diff = find_dif(list_1, list_2)
            if val_diff != "" and val_diff != "~":
              val_comps = last_different_attr_val.split("~")
              str_comps = val_diff.split("~")

              attr_name_0 = last_different_attr_name + ":" + val_comps[0]
              if not attr_name_0 in attr_dict.keys():
                attr_dict[attr_name_0] = { }
              if not str_comps[0] in attr_dict[attr_name_0].keys():
                attr_dict[attr_name_0][str_comps[0]] = 0
              attr_dict[attr_name_0][str_comps[0]] += 1

              attr_name_1 = last_different_attr_name + ":" + val_comps[1]
              if not attr_name_1 in attr_dict.keys():
                attr_dict[attr_name_1] = { }
              if not str_comps[1] in attr_dict[attr_name_1].keys():
                attr_dict[attr_name_1][str_comps[1]] = 0
              attr_dict[attr_name_1][str_comps[1]] += 1
              #if not attr_diff in attr_dict.keys():
              #  attr_dict[attr_diff] = { }
              #if not val_diff in attr_dict[attr_diff].keys():
              #  attr_dict[attr_diff][val_diff] = 0 
              #attr_dict[attr_diff][val_diff] += 1

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

          val_diff = find_dif(smaller, bigger)
          if val_diff != "" and val_diff != "~":
            val_comps = [ "", extra_val ]
            str_comps = val_diff.split("~")

            attr_name_0 = extra_attr + ":" + val_comps[0]
            if not attr_name_0 in attr_dict.keys():
              attr_dict[attr_name_0] = { }
            if not str_comps[0] in attr_dict[attr_name_0].keys():
              attr_dict[attr_name_0][str_comps[0]] = 0
            attr_dict[attr_name_0][str_comps[0]] += 1

            attr_name_1 = extra_attr + ":" + val_comps[1]
            if not attr_name_1 in attr_dict.keys():
              attr_dict[attr_name_1] = { }
            if not str_comps[1] in attr_dict[attr_name_1].keys():
              attr_dict[attr_name_1][str_comps[1]] = 0
            attr_dict[attr_name_1][str_comps[1]] += 1
            #if not attr_diff in attr_dict.keys():
            #  attr_dict[attr_diff] = { }
            #if not val_diff in attr_dict[attr_diff].keys():
            #  attr_dict[attr_diff][val_diff] = 0 
            #attr_dict[attr_diff][val_diff] += 1

for attr_type, change_list in attr_dict.items():
  print(attr_type)

  sorted_changes = sorted(change_list.items(), key = operator.itemgetter(1))

  for change, count in sorted_changes:
    print(str(count) + "\t" + change)
