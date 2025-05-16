import * as React from "react";
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { fetchFilter, FilterData, State, updateViewState } from "../State";




export class AdvancedSearch extends React.Component<{ state: State }, FilterData> {
  private fetchIds = async (data: FilterData) => {
    try {
      const url = this.props.state.channelsUrl;
      const ids = await fetchFilter(this.props.state, data);
      return ids;
    } catch (e) {
      if (e === "Not Found") {
        return [];
      }
    }
  }

  render() {
    return (
      <div className='form-group form-group-lg'>
        <Formik
          initialValues={{ minRadius: "", maxRadius: "", minDistance: "", maxDistance: "", minBottleneck: "" }}
          validate={values => {
            const errors: any = {};
            if (values.maxRadius !== "" && values.minRadius > values.maxRadius) {
              errors.minRadius = "Min radius must be less than max radius."
            }

            return errors;

          }}

          onSubmit={async (values, { setSubmitting }) => {
            // const ids = await this.fetchIds(values as FilterData)
            const ids = ['pdb_000011ba', 'pdb_00001jj2', 'P08686']
            this.props.state.fullSearch.onNext(void 0);
            updateViewState(this.props.state, { kind: 'Filter', term: ids });
          }}
        >
          {({ isSubmitting }) => (
            <Form>
              <div>
                <label>Radius</label>
                <Field label="Min Radius" type="number" min={0} name="minRadius" placeholder="Minimum Radius" />
                <ErrorMessage name="minRadius" component="div" />
                <Field type="number" min={0} name="maxRadius" placeholder="Maximum Radius" />
                <ErrorMessage name="maxRadius" component="div" />
              </div>

              <div>
                <label>Distance</label>
                <Field type="number" min={0} name="minDistance" placeholder="Minimum Distance" />
                <ErrorMessage name="minDistance" component="div" />
                <Field type="number" min={0} name="maxDistance" placeholder="Maximum Distance" />
                <ErrorMessage name="maxDistance" component="div" />
              </div>


              <div>
                <label>Bottleneck</label>
                <Field type="number" min={0} name="minBottleneck" placeholder="Minimum Bottleneck" />
                <ErrorMessage name="minBottleneck" component="div" />
              </div>

              <button type="submit" disabled={isSubmitting}>
                Submit
              </button>
            </Form>
          )}

        </Formik>
      </div>
    )
  }
}